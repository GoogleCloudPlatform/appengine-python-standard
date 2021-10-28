#!/usr/bin/env python
#
# Copyright 2007 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#




"""Sends email on behalf of the application.

This module provides functions for application developers to provide email
services for their applications. The module also provides a few utility methods.
"""










import binascii
import cgi
import codecs
from collections.abc import MutableMapping
import email
from email import parser
import email.header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import functools
import logging
import typing

from google.appengine.api import api_base_pb2
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import mail_service_pb2
from google.appengine.api import users
from google.appengine.api.mail_errors import *
from google.appengine.runtime import apiproxy_errors
import six
from six.moves import map










ERROR_MAP = {
    mail_service_pb2.MailServiceError.BAD_REQUEST:
      BadRequestError,
    mail_service_pb2.MailServiceError.UNAUTHORIZED_SENDER:
      InvalidSenderError,
    mail_service_pb2.MailServiceError.INVALID_ATTACHMENT_TYPE:
      InvalidAttachmentTypeError,
    mail_service_pb2.MailServiceError.INVALID_HEADER_NAME:
      InvalidHeaderNameError,
}







EXTENSION_MIME_MAP = {
    'aif': 'audio/x-aiff',
    'aifc': 'audio/x-aiff',
    'aiff': 'audio/x-aiff',
    'asc': 'text/plain',
    'au': 'audio/basic',
    'avi': 'video/x-msvideo',
    'bmp': 'image/x-ms-bmp',
    'c': 'text/plain',
    'css': 'text/css',
    'csv': 'text/csv',
    'doc': 'application/msword',
    'docx': 'application/msword',
    'diff': 'text/plain',
    'flac': 'audio/flac',
    'gif': 'image/gif',
    'gzip': 'application/x-gzip',
    'htm': 'text/html',
    'html': 'text/html',
    'ics': 'text/calendar',
    'jpe': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'kml': 'application/vnd.google-earth.kml+xml',
    'kmz': 'application/vnd.google-earth.kmz',
    'log': 'text/plain',
    'm4a': 'audio/mp4',
    'mid': 'audio/mid',
    'mov': 'video/quicktime',
    'mp3': 'audio/mpeg',
    'mp4': 'video/mp4',
    'mpe': 'video/mpeg',
    'mpeg': 'video/mpeg',
    'mpg': 'video/mpeg',
    'odp': 'application/vnd.oasis.opendocument.presentation',
    'ods': 'application/vnd.oasis.opendocument.spreadsheet',
    'odt': 'application/vnd.oasis.opendocument.text',
    'oga': 'audio/ogg',
    'ogg': 'audio/ogg',
    'ogv': 'video/ogg',
    'patch': 'text/plain',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'pot': 'text/plain',
    'pps': 'application/vnd.ms-powerpoint',
    'ppt': 'application/vnd.ms-powerpoint',
    'pptx': 'application/vnd.ms-powerpoint',
    'qt': 'video/quicktime',
    'rmi': 'audio/mid',
    'rss': 'text/rss+xml',
    'snd': 'audio/basic',
    'sxc': 'application/vnd.sun.xml.calc',
    'sxw': 'application/vnd.sun.xml.writer',
    'text': 'text/plain',
    'tif': 'image/tiff',
    'tiff': 'image/tiff',
    'txt': 'text/plain',
    'vcf': 'text/directory',
    'wav': 'audio/x-wav',
    'wbmp': 'image/vnd.wap.wbmp',
    'webm': 'video/webm',
    'webp': 'image/webp',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.ms-excel',
    'zip': 'application/zip',
}





EXTENSION_BLACKLIST = [
    'ade',
    'adp',
    'bat',
    'chm',
    'cmd',
    'com',
    'cpl',
    'exe',
    'hta',
    'ins',
    'isp',
    'jse',
    'lib',
    'mde',
    'msc',
    'msp',
    'mst',
    'pif',
    'scr',
    'sct',
    'shb',
    'sys',
    'vb',
    'vbe',
    'vbs',
    'vxd',
    'wsc',
    'wsf',
    'wsh',
]


HEADER_WHITELIST = frozenset([
    'Auto-Submitted',
    'In-Reply-To',
    'List-Id',
    'List-Unsubscribe',
    'On-Behalf-Of',
    'References',
    'Resent-Date',
    'Resent-From',
    'Resent-To',
])

INCOMING_MAIL_URL_PATTERN = '/_ah/mail/.+'
BOUNCE_NOTIFICATION_URL_PATH = '/_ah/bounce'


def invalid_email_reason(email_address, field):
  """Determines the reason why an email is invalid.

  Args:
    email_address: Email address to check.
    field: Field that is invalid.

  Returns:
    A string that indicates the reason why an email is invalid; otherwise
    returns `None`.
  """
  if email_address is None:
    return 'None email address for %s.' % field

  if isinstance(email_address, users.User):
    email_address = email_address.email()
  if not isinstance(email_address, six.string_types):
    return 'Invalid email address type for %s.' % field
  stripped_address = email_address.strip()
  if not stripped_address:
    return 'Empty email address for %s.' % field
  return None


InvalidEmailReason = invalid_email_reason


def is_email_valid(email_address):
  """Determines whether an email address is invalid.

  Args:
    email_address: Email address to check.

  Returns:
    `True` if the specified email address is valid; otherwise returns `False`.
  """
  return invalid_email_reason(email_address, '') is None


IsEmailValid = is_email_valid


def check_email_valid(email_address, field):
  """Verifies whether an email is valid.

  Args:
    email_address: Email address to check.
    field: Field to check.

  Raises:
    InvalidEmailError: If `email_address` is invalid.
  """
  reason = invalid_email_reason(email_address, field)
  if reason is not None:
    raise InvalidEmailError(reason)


CheckEmailValid = check_email_valid


def is_ascii(string):
  """Returns whether a string is in ASCII."""
  return all(ord(c) < 128 for c in string)


def invalid_headers_reason(headers):
  """Determines the reason why a header is invalid.

  Args:
    headers: Header value to check.

  Returns:
    A string that indicates the reason that the headers are invalid if the
    reason can be determined; otherwise returns `None`.
  """
  if headers is None:
    return 'Headers dictionary was None.'
  if not isinstance(headers, dict):
    return 'Invalid type for headers. Should be a dictionary.'
  for k, v in six.iteritems(headers):
    if not isinstance(k, six.string_types):
      return 'Header names should be strings.'
    if not isinstance(v, six.string_types):
      return 'Header values should be strings.'
    if not is_ascii(k):
      return 'Header name should be an ASCII string.'

    if k.strip() not in HEADER_WHITELIST:
      return 'Header "%s" is not allowed.' % k.strip()


def check_headers_valid(headers):
  """Checks that `headers` is a valid dictionary for a header.

  Args:
    headers: The value to check for the headers.

  Raises:
    InvalidEmailError: If `headers` is invalid.
  """
  reason = invalid_headers_reason(headers)
  if reason is not None:
    raise InvalidEmailError(reason)


def _email_sequence(emails):
  """Forces an email to be a sequenceable type.

  Iterable values are returned as-is. This function really just wraps the case
  where there is a single email string.

  Args:
    emails: At least one email address to coerce to sequence.

  Returns:
    A single tuple that contains the email address if only one email string is
    provided; otherwise returns email addresses as-is.
  """
  if isinstance(emails, six.string_types):
    return [email_address.strip() for email_address in emails.split(',')]
  return emails


def _attachment_sequence(attachments):
  """Forces attachments to be a sequenceable type.

  Iterable values are returned as-is. This function really just wraps the case
  where there is a single attachment.

  Args:
    attachments: Attachments (or attachment) to coerce to sequence.

  Yields:
    A single tuple that contains the attachment if only one attachment is
    provided; otherwise returns attachments as-is.
  """
  if len(attachments) == 2 and isinstance(attachments[0], six.string_types):
    attachments = attachments,
  for attachment in attachments:
    if isinstance(attachment, Attachment):
      yield attachment
    else:
      yield Attachment(*attachment)


def _parse_mime_message(
    mime_message: typing.Union[typing.Text, bytes, typing.TextIO,
                               email.message.Message]
) -> email.message.Message:
  """Helper function that converts `mime_message` into `email.message.Message`.

  Args:
    mime_message: MIME message, string, or file that contains the MIME
    message.

  Returns:
    An instance of `email.message.Message`. This method will return
    the `mime_message` if the instance already exists.
  """
  if isinstance(mime_message, email.message.Message):
    return mime_message
  elif isinstance(mime_message, six.string_types):

    return email.message_from_string(mime_message)
  elif isinstance(mime_message, bytes):
    return email.message_from_bytes(mime_message)
  else:

    return email.message_from_file(mime_message)


def send_mail(sender,
              to,
              subject,
              body,
              make_sync_call=apiproxy_stub_map.MakeSyncCall,
              **kw):
  """Sends mail on behalf of the application.

  Args:
    sender: Sender email address as it appears in the 'From' email line.
    to: List of one or more 'To' addresses.
    subject: Message subject string.
    body: Plain-text body.
    make_sync_call: Function used to make a sync call to an API proxy.
    **kw: Keyword arguments that are compatible with the `EmailMessage`
        keyword based constructor.

  Raises:
    InvalidEmailError: If an invalid email address was specified.
  """
  kw['sender'] = sender
  kw['to'] = to
  kw['subject'] = subject
  kw['body'] = body
  message = EmailMessage(**kw)
  message.send(make_sync_call=make_sync_call)


SendMail = send_mail


def send_mail_to_admins(sender,
                        subject,
                        body,
                        make_sync_call=apiproxy_stub_map.MakeSyncCall,
                        **kw):
  """Sends email to administrators on behalf of the application.

  Args:
    sender: Sender email address as it appears in the 'From' email line.
    subject: Message subject string.
    body: Plain-text body.
    make_sync_call: Function used to make a sync call to an API proxy.
    **kw: Keyword arguments that are compatible with the `EmailMessage` keyword
        based constructor.

  Raises:
    InvalidEmailError: If an invalid email address was specified.
  """
  kw['sender'] = sender
  kw['subject'] = subject
  kw['body'] = body
  message = AdminEmailMessage(**kw)
  message.send(make_sync_call=make_sync_call)


SendMailToAdmins = send_mail_to_admins


def _GetMimeType(file_name):
  """Determines the `MINE` type from the file name.

  This function parses the file name and determines the MIME type based on
  an extension map.

  This method is not part of the public API and should not be used by
  applications.

  Args:
    file_name: File for which you are attempting to determine the extension.

  Returns:
    The MIME type that is associated with the file extension.

  Raises:
    InvalidAttachmentTypeError: If the file type is invalid.
  """
  extension_index = file_name.rfind('.')
  if extension_index == -1:
    extension = ''
  else:
    extension = file_name[extension_index + 1:].lower()
  if extension in EXTENSION_BLACKLIST:
    raise InvalidAttachmentTypeError(
        'Extension %s is not supported.' % extension)
  mime_type = EXTENSION_MIME_MAP.get(extension, None)
  if mime_type is None:
    mime_type = 'application/octet-stream'
  return mime_type


def _GuessCharset(text):
  """Guesses the character set of a piece of text.

  Args:
    text: A string that is either a US-ASCII string or a Unicode string that was
        encoded in UTF-8.

  Returns:
    The character set that is needed by the string, either US-ASCII or UTF-8.
  """
  if isinstance(text, six.text_type):
    try:
      text.encode('us-ascii')
      return 'us-ascii'
    except UnicodeEncodeError:
      return 'utf-8'

  else:
    try:
      text.decode('us-ascii')
      return 'us-ascii'
    except UnicodeDecodeError:
      return 'utf-8'


def _I18nHeader(text):
  """Creates a properly encoded header, even with Unicode content.

  Args:
    text: A string that is either a US-ASCII string or a Unicode string that was
        encoded in UTF-8.
  Returns:
    The properly encoded `email.header.Header`.
  """
  charset = _GuessCharset(text)
  return email.header.Header(text, charset, maxlinelen=1e3000)


def mail_message_to_mime_message(protocol_message):
  """Generates a `MIMEMultipart` message from a `MailMessage` protocol buffer.

  This function generates a complete `MIMEMultipart` email object from a
  `MailMessage` protocol buffer. The body fields are sent as individual
  alternatives if they are both present; otherwise, only one body part is sent.

  Multiple entry email fields, such as 'To', 'Cc', and 'Bcc' are converted
  to a list of comma-separated email addresses.

  Args:
    protocol_message: Message protocol buffer to convert to a `MIMEMultipart`
        message.

  Returns:
    A `MIMEMultipart` message that represents the provided `MailMessage`.

  Raises:
    InvalidAttachmentTypeError: If the file type of the attachment is invalid.
  """
  parts = []
  if protocol_message.HasField('TextBody'):
    parts.append(
        MIMEText(
            protocol_message.TextBody,
            _charset=_GuessCharset(protocol_message.TextBody)))
  if protocol_message.HasField('AmpHtmlBody'):
    parts.append(
        MIMEText(
            protocol_message.AmpHtmlBody,
            _subtype='x-amp-html',
            _charset=_GuessCharset(protocol_message.AmpHtmlBody)))
  if protocol_message.HasField('HtmlBody'):
    parts.append(
        MIMEText(
            protocol_message.HtmlBody,
            _subtype='html',
            _charset=_GuessCharset(protocol_message.HtmlBody)))

  if len(parts) == 1:

    payload = parts
  else:

    payload = [MIMEMultipart('alternative', _subparts=parts)]

  result = MIMEMultipart(_subparts=payload)

  for attachment in protocol_message.Attachment:
    file_name = attachment.FileName
    mime_type = _GetMimeType(file_name)
    maintype, subtype = mime_type.split('/')
    mime_attachment = MIMEBase(maintype, subtype)
    mime_attachment.add_header(
        'Content-Disposition', 'attachment', filename=attachment.FileName)
    mime_attachment.set_payload(attachment.Data)
    if attachment.HasField('ContentID'):
      mime_attachment['content-id'] = attachment.ContentID
    result.attach(mime_attachment)


  if protocol_message.To:
    result['To'] = _I18nHeader(', '.join(protocol_message.To))
  if protocol_message.Cc:
    result['Cc'] = _I18nHeader(', '.join(protocol_message.Cc))
  if protocol_message.Bcc:
    result['Bcc'] = _I18nHeader(', '.join(protocol_message.Bcc))

  result['From'] = _I18nHeader(protocol_message.Sender)
  result['Reply-To'] = _I18nHeader(protocol_message.ReplyTo)
  result['Subject'] = _I18nHeader(protocol_message.Subject)

  for header in protocol_message.Header:
    result[header.name] = _I18nHeader(header.value)

  return result


MailMessageToMIMEMessage = mail_message_to_mime_message


def _to_str(value):
  """Helper function to ensure that Unicode values are converted to UTF-8.

  Args:
    value: String or Unicode to convert to UTF-8.

  Returns:
    The UTF-8 encoded string of `value`; `value` remains otherwise unchanged.
  """
  if isinstance(value, six.text_type):
    return value.encode('utf-8')
  return value


def _decode_and_join_header(header, separator=u' '):
  """Helper function to decode RFC2047 encoded headers.

  Args:
    header: `RFC2047`_ encoded string (or just a standard string) to convert to
        Unicode.
    separator: The separator to use when joining separately encoded pieces of
        the header.

  Returns:
    The Unicode version of the decoded header; returns `None` or `''` if the
    header is not set.

  .. _RFC2047:
     https://www.ietf.org/rfc/rfc2047.txt
  """
  if not header:

    return header

  def header_gen(header_string):
    """Generate a sequence of header from header string.

    A generator that consume header string and return a sequence of header in
    decoded format (PY2: str; PY3: unicode).

    Args:
      header_string: A string that contains multiline of headers.

    Yields:
      string
    """


    for s, charset in email.header.decode_header(header_string):
      if not charset:
        charset = 'us-ascii'



      if isinstance(s, bytes):
        yield codecs.decode(s, charset, 'replace')
      else:
        yield s

  return separator.join(header_gen(header))


def _decode_address_list_field(address_list):
  """Helper function to decode (potentially RFC2047 encoded) address lists.

  Args:
    address_list: A single string header, or list of string headers.

  Returns:
    The Unicode version of a decoded header or a list of string headers.
  """
  if not address_list:
    return None

  if len(address_list) == 1:
    return _decode_and_join_header(address_list[0])
  else:
    return list(map(_decode_and_join_header, address_list))




def _wrapping(wrapped):
  """A decorator that decorates a decorator's wrapper.

  This decorator makes it easier to debug code that is heavily decorated.

  Args:
    wrapped: The decorated function that you are trying to debug.

  Returns:
    A function with `__name__`, `__doc__`, and `___dict__` remapped to the
    respective versions of the wrapped function to make debugging easier.
  """




  def wrapping_wrapper(wrapper):
    try:
      wrapper.__wrapped__ = wrapped
      wrapper.__name__ = wrapped.__name__
      wrapper.__doc__ = wrapped.__doc__
      wrapper.__dict__.update(wrapped.__dict__)
    except Exception:
      pass
    return wrapper
  return wrapping_wrapper








wrapping = _wrapping if six.PY2 else functools.wraps



def _positional(max_pos_args):
  """A decorator to declare that only the first N arguments can be positional.

  Note:
      For methods, N includes 'self'.

  Args:
    max_pos_args: The number of arguments that can be positional.

  Returns:
    The wrapped object, but verifies that the wrapped object does not have more
    than `max_pos_args`. If the object does contain more than `max_pos_args`
    arguments, a `TypeError` is raised.
  """
  def positional_decorator(wrapped):
    @functools.wraps(wrapped)
    def positional_wrapper(*args, **kwds):
      if len(args) > max_pos_args:
        plural_s = ''
        if max_pos_args != 1:
          plural_s = 's'
        raise TypeError(
            '%s() takes at most %d positional argument%s (%d given)' %
            (wrapped.__name__, max_pos_args, plural_s, len(args)))
      return wrapped(*args, **kwds)
    return positional_wrapper
  return positional_decorator


class Attachment(object):
  """Attachment object.

  An Attachment object is largely interchangeable with a `(filename, payload)`
  tuple.

  Note:
      The behavior is a bit asymmetric with respect to unpacking and equality
      comparison. An Attachment object without a content ID will be equivalent
      to a `(filename, payload)` tuple. An Attachment with a content ID will
      unpack to a `(filename, payload)` tuple, but will compare unequally to
      that tuple.

      Thus, the following comparison will succeed:

          attachment = mail.Attachment('foo.jpg', 'data')
          filename, payload = attachment
          attachment == filename, payload


      ...while the following will fail:

          attachment = mail.Attachment('foo.jpg', 'data', content_id='<foo>')
          filename, payload = attachment
          attachment == filename, payload


      The following comparison will pass:

        attachment = mail.Attachment('foo.jpg', 'data', content_id='<foo>')
        attachment == (attachment.filename,
                       attachment.payload,
                       attachment.content_id)

  Attributes:
    filename: The name of the attachment.
    payload: The attachment data.
    content_id: Optional; the content ID for this attachment. Keyword only.
  """

  @_positional(3)
  def __init__(self, filename, payload, content_id=None):
    """Constructor.

    Arguments:
      filename: The name of the attachment.
      payload: The attachment data.
      content_id: Optional; the content ID for this attachment.
    """
    self.filename = filename
    self.payload = payload
    self.content_id = content_id

  def __eq__(self, other):
    self_tuple = (self.filename, self.payload, self.content_id)
    if isinstance(other, Attachment):
      other_tuple = (other.filename, other.payload, other.content_id)


    elif not hasattr(other, '__len__'):
      return NotImplemented
    elif len(other) == 2:
      other_tuple = other + (None,)
    elif len(other) == 3:
      other_tuple = other
    else:
      return NotImplemented
    return self_tuple == other_tuple

  def __hash__(self):
    if self.content_id:
      return hash((self.filename, self.payload, self.content_id))
    else:
      return hash((self.filename, self.payload))

  def __ne__(self, other):
    return not self == other

  def __iter__(self):
    return iter((self.filename, self.payload))

  def __getitem__(self, i):
    return tuple(iter(self))[i]

  def __contains__(self, val):
    return val in (self.filename, self.payload)

  def __len__(self):
    return 2


class EncodedPayload(object):
  """Wrapper for a payload that contains encoding information.

  When an email is received, it is usually encoded using a certain character
  set, then possibly further encoded using a transfer encoding in that
  character set. Most of the time, it is possible to decode the encoded
  payload as-is; however, in the case where it is not, the encoded payload and
  the original encoding information must be preserved.

  Attributes:
    payload: The original encoded payload.
    charset: The character set of the encoded payload. To specify that you want
        to use the default character set, set this argument to `None`.
    encoding: The transfer encoding of the encoded payload. To specify that you
        do not want the content to be encoded, set this argument to `None`.
  """

  def __init__(self, payload: bytes, charset=None, encoding=None):
    """Constructor.

    Args:
      payload: Maps to an attribute of the same name.
      charset: Maps to an attribute of the same name.
      encoding: Maps to an attribute of the same name.
    """
    if not isinstance(payload, bytes):
      raise TypeError('EncodedPayload must be bytes, but got ' + type(payload))

    self.payload = payload
    self.charset = charset
    self.encoding = encoding

  def decode(self):
    """Attempts to decode the encoded data.

    This function attempts to use `Python's codec library`_ to decode the
    payload. All exceptions are passed back to the caller.

    Returns:
      The binary or Unicode version of the payload content.

    .. _Python's codec library:
       https://docs.python.org/2/library/codecs.html
    """
    payload = self.payload


    if self.encoding and self.encoding.lower() not in ('7bit', '8bit'):
      try:
        payload = codecs.decode(payload, self.encoding)
      except LookupError:
        raise UnknownEncodingError('Unknown decoding %s.' % self.encoding)
      except (Exception, Error) as e:
        raise PayloadEncodingError('Could not decode payload: %s' % e)


    if self.charset and str(self.charset).lower() != '7bit':
      try:
        payload = codecs.decode(payload, str(self.charset))
      except LookupError:
        raise UnknownCharsetError('Unknown charset %s.' % self.charset)
      except (Exception, Error) as e:
        raise PayloadEncodingError('Could read characters: %s' % e)
    return payload

  def __eq__(self, other):
    """Equality operator.

    Args:
      other: The other `EncodedPayload` object with which to compare. Comparison
          with other object types are not implemented.

    Returns:
      `True` if the payload and encodings are equal; otherwise returns `False`.
    """
    if isinstance(other, EncodedPayload):
      return (self.payload == other.payload and
              self.charset == other.charset and
              self.encoding == other.encoding)
    else:
      return NotImplemented

  def __hash__(self):
    """Hashes an `EncodedPayload`."""
    return hash((self.payload, self.charset, self.encoding))

  def copy_to(self, mime_message):
    """Copies the contents of a message to a MIME message payload.

    If no content transfer encoding is specified and the character set does not
    equal the overall message encoding, the payload will be base64-encoded.

    Args:
      mime_message: Message instance that will receive the new payload.
    """
    if self.encoding:
      mime_message['content-transfer-encoding'] = self.encoding
    mime_message.set_payload(self.payload, self.charset)

  def to_mime_message(self):
    """Converts a message to a MIME message.

    Returns:
      The MIME message instance of the payload.
    """
    mime_message = email.message.Message()
    self.copy_to(mime_message)
    return mime_message

  def __str__(self):
    """String representation of an encoded message.

    Returns:
      The MIME encoded representation of an encoded payload as an independent
      message.
    """
    return str(self.to_mime_message())

  def __repr__(self):
    """Represents an encoded payload.

    Returns:
      The payload itself as represented by its hash value.
    """
    result = '<EncodedPayload payload=#%d' % hash(self.payload)
    if self.charset:
      result += ' charset=%s' % self.charset
    if self.encoding:
      result += ' encoding=%s' % self.encoding
    return result + '>'


class _EmailMessageBase(object):
  """Base class for Mail API service objects.

  Subclasses must define a class variable called `_API_CALL` with the name of
  its underlying mail-sending API call.
  """


  PROPERTIES = set([
      'sender',
      'reply_to',
      'subject',
      'body',
      'html',
      'amp_html',
      'attachments',
  ])

  ALLOWED_EMPTY_PROPERTIES = set([
      'subject',
      'body',
      'amp_html',
  ])



  PROPERTIES.update(('to', 'cc', 'bcc'))

  def __init__(self, mime_message=None, **kw):
    """Initializes an email message.

    This initializer creates a new `MailMessage` protocol buffer and initializes
    it with any keyword arguments.

    Args:
      mime_message: The MIME message to initialize from. If the message is an
          instance of `email.message.Message`, `mime_message` will take
          ownership as specified the original message.
      **kw: List of keyword properties as defined by `PROPERTIES`.
    """
    if mime_message:
      mime_message = _parse_mime_message(mime_message)
      self.update_from_mime_message(mime_message)
      self.__original = mime_message



    self.initialize(**kw)

  @property
  def original(self):
    """Gets the original MIME message from which values were set."""
    return self.__original

  def initialize(self, **kw):
    """Keyword initialization.

    This function sets all fields of the email message using the keyword
    arguments.

    Args:
      **kw: List of keyword properties as defined by `PROPERTIES`.
    """
    for name, value in six.iteritems(kw):
      setattr(self, name, value)


  def Initialize(self, **kw):
    self.initialize(**kw)

  def check_initialized(self):
    """Checks if `EmailMessage` is properly initialized.

    This function tests if `EmailMessage` meets the basic requirements to be
    used with the Mail API. To function properly, this function requires that
    the following fields must be set or have at least one value in the case of
    multi-value fields:
        - A subject must be set.
        - A recipient must be specified.
        - The message must contain a body.
        - All bodies and attachments must decode properly.

    This test does not include determining if the sender is actually authorized
    to send email for the application.

    Raises:
      InvalidAttachmentTypeError: The attachment type is invalid.
      MissingRecipientsError: No recipients were specified in the 'To', 'Cc', or
          'Bcc' fields.
      MissingSenderError: A sender was not specified.
      MissingSubjectError: A subject was not specified.
      MissingBodyError: A body was not specified.
      PayloadEncodingError: The payload was not properly encoded.
      UnknownEncodingError: The payload encoding could not be determined.
      UnknownCharsetError: The character set of the payload could not be
          determined.
    """
    if not hasattr(self, 'sender'):
      raise MissingSenderError()


    found_body = False

    try:
      body = self.body
    except AttributeError:
      pass
    else:
      if isinstance(body, EncodedPayload):

        body.decode()
      found_body = True

    try:
      html = self.html
    except AttributeError:
      pass
    else:
      if isinstance(html, EncodedPayload):

        html.decode()
      found_body = True

    try:
      amp_html = self.amp_html
    except AttributeError:
      pass
    else:
      if isinstance(amp_html, EncodedPayload):

        amp_html.decode()

    if hasattr(self, 'attachments'):
      for attachment in _attachment_sequence(self.attachments):


        _GetMimeType(attachment.filename)




        if isinstance(attachment.payload, EncodedPayload):
          attachment.payload.decode()


  def CheckInitialized(self):
    """Ensures that recipients have been specified."""
    self.check_initialized()

  def is_initialized(self):
    """Determines if `EmailMessage` is properly initialized.

    Returns:
      `True` if the message is properly initialized; otherwise returns `False`.
    """
    try:
      self.check_initialized()
      return True
    except Error:
      return False


  def IsInitialized(self):
    """Determines if `EmailMessage` is properly initialized."""
    return self.is_initialized()

  def ToProto(self):
    """Converts an email message to a protocol message.

    Unicode strings are converted to UTF-8 for all fields.

    This method is overridden by `EmailMessage` to support the sender field.

    Returns:
      The `MailMessage` protocol version of the mail message.

    Raises:
      Decoding errors when using `EncodedPayload` objects.
    """
    self.check_initialized()
    message = mail_service_pb2.MailMessage()
    message.Sender = _to_str(self.sender)

    if hasattr(self, 'reply_to'):
      message.ReplyTo = _to_str(self.reply_to)
    if hasattr(self, 'subject'):
      message.Subject = _to_str(self.subject)
    else:
      message.Subject = ''

    if hasattr(self, 'body'):
      body = self.body
      if isinstance(body, EncodedPayload):
        body = body.decode()
      message.TextBody = _to_str(body)

    if hasattr(self, 'html'):
      html = self.html
      if isinstance(html, EncodedPayload):
        html = html.decode()
      message.HtmlBody = _to_str(html)

    if hasattr(self, 'amp_html'):
      amp_html = self.amp_html
      if isinstance(amp_html, EncodedPayload):
        amp_html = amp_html.decode()
      message.AmpHtmlBody = _to_str(amp_html)

    if hasattr(self, 'attachments'):
      for attachment in _attachment_sequence(self.attachments):
        if isinstance(attachment.payload, EncodedPayload):
          attachment.payload = attachment.payload.decode()
        protoattachment = message.Attachment.add()
        protoattachment.FileName = _to_str(attachment.filename)
        protoattachment.Data = _to_str(attachment.payload)
        if attachment.content_id:
          protoattachment.ContentID = attachment.content_id
    return message

  def to_mime_message(self):
    """Generates a `MIMEMultipart` message from `EmailMessage`.

    This function calls `MailMessageToMessage` after converting `self` to
    the protocol buffer. The protocol buffer is better at handing corner cases
    than the `EmailMessage` class.

    Returns:
      A `MIMEMultipart` message that represents the provided `MailMessage`.

    Raises:
      InvalidAttachmentTypeError: The attachment type was invalid.
      MissingSenderError: A sender was not specified.
      MissingSubjectError: A subject was not specified.
      MissingBodyError: A body was not specified.
    """
    return mail_message_to_mime_message(self.ToProto())


  def ToMIMEMessage(self):
    return self.to_mime_message()

  def send(self, make_sync_call=apiproxy_stub_map.MakeSyncCall):
    """Sends an email message via the Mail API.

    Args:
      make_sync_call: Method that will make a synchronous call to the API proxy.
    """
    message = self.ToProto()
    response = api_base_pb2.VoidProto()

    try:
      make_sync_call('mail', self._API_CALL, message, response)
    except apiproxy_errors.ApplicationError as e:
      if e.application_error in ERROR_MAP:
        raise ERROR_MAP[e.application_error](e.error_detail)
      raise e


  def Send(self, *args, **kwds):
    self.send(*args, **kwds)

  def _check_attachment(self, attachment):

    if not (isinstance(attachment.filename, six.string_types) or
            isinstance(attachment.payload, six.string_types)):
      raise TypeError()

  def _check_attachments(self, attachments):
    """Checks the values that are going to the attachment field.

    This function is mainly used to check type safety of the values. Each value
    of the list must be a pair of the form `(file_name, data)`, and both values
    must use a string type.

    Args:
      attachments: Collection of attachment tuples.

    Raises:
      TypeError: If values do not use the string data type.
    """
    attachments = _attachment_sequence(attachments)
    for attachment in attachments:
      self._check_attachment(attachment)

  def __setattr__(self, attr, value):
    """Property that sets access control.

    This function controls write access to email fields.

    Args:
      attr: Attribute to access.
      value: The new value for the field.

    Raises:
      ValueError: If a value was not specified.
      AttributeError: If the attribute is not an allowed assignment field.
    """
    if not attr.startswith('_EmailMessageBase'):
      if attr in ['sender', 'reply_to']:
        check_email_valid(value, attr)

      if not value and attr not in self.ALLOWED_EMPTY_PROPERTIES:
        raise ValueError('May not set empty value for \'%s\'' % attr)


      if attr not in self.PROPERTIES:
        raise AttributeError('\'EmailMessage\' has no attribute \'%s\'' % attr)


      if attr == 'attachments':
        self._check_attachments(value)

    super(_EmailMessageBase, self).__setattr__(attr, value)

  def _add_body(self, content_type, payload):
    """Adds a body to an email from the payload.

    This function will overwrite any existing default plain or HTML body.

    Args:
      content_type: Content type of the body.
      payload: Payload to store the body as.
    """

    if content_type == 'text/plain':
      self.body = payload
    elif content_type == 'text/html':
      self.html = payload

  def _update_payload(self, mime_message: email.message.Message):
    """Updates a payload of a mail message from `mime_message`.

    This function works recursively when it receives a multi-part body. If the
    function receives a non-multi-part MIME object, it will determine whether
    it is an attachment by whether it contains a file name. Attachments and
    bodies are then wrapped in `EncodedPayload` that use the correct character
    sets and encodings.

    Args:
      mime_message: A Message MIME email object.
    """
    payload = mime_message.get_payload()

    if payload:
      if mime_message.is_multipart():
        for alternative in payload:
          self._update_payload(alternative)
      else:
        filename = mime_message.get_param('filename',
                                          header='content-disposition')
        if filename:

          filename = email.utils.collapse_rfc2231_value(filename)
        if not filename:
          filename = mime_message.get_param('name')


        encoded_payload = EncodedPayload(
            six.ensure_binary(payload),
            (mime_message.get_content_charset() or mime_message.get_charset()),
            mime_message['content-transfer-encoding'])

        if 'content-id' in mime_message:
          attachment = Attachment(
              filename, encoded_payload, content_id=mime_message['content-id'])
        else:
          attachment = Attachment(filename, encoded_payload)

        if filename:

          try:
            attachments = self.attachments
          except AttributeError:
            self.attachments = [attachment]
          else:
            if isinstance(attachments[0], six.string_types):
              self.attachments = [attachments]
              attachments = self.attachments
            attachments.append(attachment)
        else:
          self._add_body(mime_message.get_content_type(), encoded_payload)

  def update_from_mime_message(self, mime_message):
    """Copies information from a MIME message.

    Information from the `email.Message` instance is set to the values of the
    MIME message. This function will only copy values that it finds. Missing
    values will not be copied, nor will those values overwrite old values with
    blank values.

    This object is not guaranteed to be initialized after this call.

    Args:
      mime_message: The `email.Message` instance from which to copy information.

    Returns:
      A MIME message instance of the `mime_message`.
    """
    mime_message = _parse_mime_message(mime_message)

    sender = _decode_and_join_header(mime_message['from'])
    if sender:
      self.sender = sender

    reply_to = _decode_and_join_header(mime_message['reply-to'])
    if reply_to:
      self.reply_to = reply_to

    subject = _decode_and_join_header(mime_message['subject'], separator=u'')
    if subject:
      self.subject = subject

    self._update_payload(mime_message)

  def bodies(self, content_type: typing.Text = None):
    """Iterates over all bodies.

    Args:
      content_type: Content type on which to filter. This argument allows you to
          select only specific types of content. You can use the base type or
          the content type.

          For example:

              content_type = 'text/html'  # Matches only HTML content.
              content_type = 'text'       # Matches text of any kind.

    Yields:
      A `(content_type, payload)` tuple for HTML and body in that order.
    """
    if (not content_type or
        content_type == 'text' or
        content_type == 'text/html'):
      try:
        yield 'text/html', self.html
      except AttributeError:
        pass

    if (not content_type or
        content_type == 'text' or
        content_type == 'text/plain'):
      try:
        yield 'text/plain', self.body
      except AttributeError:
        pass


class EmailMessage(_EmailMessageBase):
  """Main interface to the Mail API service.

  This class is used to programmatically build an email message to send via the
  Mail API. To use this class, construct an instance, populate its fields and
  call `Send()`.

  An `EmailMessage` can be built completely by the constructor:

      EmailMessage(sender='sender@nowhere.com',
                   to='recipient@nowhere.com',
                   subject='a subject',
                   body='This is an email to you').Send()


  You might want your application to build an email in different places
  throughout the code. For this usage, `EmailMessage` is mutable:

        message = EmailMessage()
        message.sender = 'sender@nowhere.com'
        message.to = ['recipient1@nowhere.com', 'recipient2@nowhere.com']
        message.subject = 'a subject'
        message.body = 'This is an email to you'
        message.check_initialized()
        message.send()
  """

  _API_CALL = 'Send'
  PROPERTIES = set(_EmailMessageBase.PROPERTIES | set(('headers',)))


  def __init__(
      self,
      mime_message: typing.Optional[typing.Union[typing.Text, bytes,
                                                 typing.TextIO,
                                                 email.message.Message]] = None,
      **kw):
    """
    """


    super().__init__(mime_message, **kw)


  def check_initialized(self):
    """Provides additional checks to ensure that recipients have been specified.

    Raises:
      MissingRecipientError: If no recipients are specified in 'To', 'Cc', or
          'Bcc'.
    """
    if (not hasattr(self, 'to') and
        not hasattr(self, 'cc') and
        not hasattr(self, 'bcc')):
      raise MissingRecipientsError()
    super(EmailMessage, self).check_initialized()


  def CheckInitialized(self):
    """Ensures that recipients have been specified."""
    self.check_initialized()

  def ToProto(self):
    """Performs more conversion of recipient fields to the protocol buffer.

    Returns:
      The `MailMessage` protocol version of the mail message, including sender
      fields.
    """
    message = super(EmailMessage, self).ToProto()

    for attribute, adder in (('to', message.To.append),
                             ('cc', message.Cc.append), ('bcc',
                                                         message.Bcc.append)):
      if hasattr(self, attribute):
        for address in _email_sequence(getattr(self, attribute)):
          adder(_to_str(address))
    for name, value in six.iteritems(getattr(self, 'headers', {})):
      header = message.Header.add()
      header.name = name
      header.value = _to_str(value)
    return message

  def __setattr__(self, attr, value):
    """Performs additional checks on recipient fields."""

    if attr in ['to', 'cc', 'bcc']:
      if isinstance(value, six.string_types):
        if value == '' and getattr(self, 'ALLOW_BLANK_EMAIL', False):
          return
        check_email_valid(value, attr)
      else:
        for address in value:
          check_email_valid(address, attr)
    elif attr == 'headers':
      check_headers_valid(value)

    super(EmailMessage, self).__setattr__(attr, value)

  def update_from_mime_message(self, mime_message):
    """Copies information for recipients from a MIME message.

    Args:
      mime_message: The `email.Message` instance from which to copy information.
    """
    mime_message = _parse_mime_message(mime_message)
    super(EmailMessage, self).update_from_mime_message(mime_message)

    to = _decode_address_list_field(mime_message.get_all('to'))
    if to:
      self.to = to

    cc = _decode_address_list_field(mime_message.get_all('cc'))
    if cc:
      self.cc = cc

    bcc = _decode_address_list_field(mime_message.get_all('bcc'))
    if bcc:
      self.bcc = bcc


class AdminEmailMessage(_EmailMessageBase):
  """Interface that sends email messages to all administrators via the Mail API.

  This class is used to programmatically build an administrator email message to
  be sent via the Mail API. To use the class, construct an instance, populate
  its fields, and call `Send()`.

  Unlike normal email messages, addresses in the recipient fields are ignored
  and not used to send the message.

  An `AdminEmailMessage` can be built completely by the constructor:

      AdminEmailMessage(sender='sender@nowhere.com',
                        subject='a subject',
                        body='This is an email to you').Send()


  You might want your application to build an administrator email in different
  places throughout the code. For this, `AdminEmailMessage` is mutable:

      message = AdminEmailMessage()
      message.sender = 'sender@nowhere.com'
      message.subject = 'a subject'
      message.body = 'This is an email to you'
      message.check_initialized()
      message.send()
  """

  _API_CALL = 'SendToAdmins'
  __UNUSED_PROPERTIES = set(('to', 'cc', 'bcc'))

  def __setattr__(self, attr, value):
    if attr in self.__UNUSED_PROPERTIES:
      logging.warning('\'%s\' is not a valid property to set '
                      'for AdminEmailMessage.  It is unused.', attr)
    super(AdminEmailMessage, self).__setattr__(attr, value)


class InboundEmailMessage(EmailMessage):
  """Receives a parsed email as it is recevied from an external source.

  This class makes use of a `date` field and can store any number of additional
  bodies. These additional attributes make the email more flexible as required
  for incoming mail, where the developer has less control over the content.

  Example:

      # Read mail message from `CGI` input.
      message = InboundEmailMessage(sys.stdin.read())
      logging.info('Received email message from %s at %s',
                   message.sender,
                   message.date)
      enriched_body = list(message.bodies('text/enriched'))[0]
      # ... Do something with body ...
  """

  __HEADER_PROPERTIES = {
      'date': 'date',
      'message_id': 'message-id',
  }

  PROPERTIES = frozenset(_EmailMessageBase.PROPERTIES
                         | set(('alternate_bodies',))
                         | set(six.iterkeys(__HEADER_PROPERTIES)))

  ALLOW_BLANK_EMAIL = True

  @classmethod
  def from_environ(cls, environ):
    """Creates an email message by parsing the HTTP request body in `environ`.

    Example (WSGI)::

      def app(environ, start_response):
        mail_message = mail.InboundEmailMessage.from_environ(request.environ)

        # Do something with the message
        logging.info('Received greeting from %s: %s' % (mail_message.sender,
                                                          mail_message.body))
        start_response("200 OK", [])
        return “Success”

    Note: Flask (other web frameworks) can directly use
          `new InboundEmailMessage(request_bytes)` to create the email message
          if they have the request bytes of an HTTP request.

    Args:
      environ: a WSGI dict describing the HTTP request (See PEP 333).
    Returns:
      An InboundEmailMessage object.
    """
    try:
      req_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
      req_size = 0

    request_bytes = environ['wsgi.input'].read(req_size)
    return InboundEmailMessage(request_bytes)

  def update_from_mime_message(self, mime_message):
    """Updates the values of a MIME message.

    This function copies over date values.

    Args:
      mime_message: The `email.Message` instance from which you want to copy
        information.
    """
    mime_message = _parse_mime_message(mime_message)
    super(InboundEmailMessage, self).update_from_mime_message(mime_message)

    for property_, header in six.iteritems(
        InboundEmailMessage.__HEADER_PROPERTIES):
      value = mime_message[header]
      if value:
        setattr(self, property_, value)

  def _add_body(self, content_type, payload):
    """Adds a body to an inbound message.

    This method is overidden to handle incoming messages that have more than one
    plain or HTML body or have any unidentified bodies.

    This method will not overwrite existing HTML and body values. Therefore,
    when the message is updated with the body, the text and HTML bodies that
    are first in the MIME document order are assigned to the body and HTML
    properties.

    Args:
      content_type: Content type of the additional body.
      payload: Content of the additional body.
    """
    if (content_type == 'text/plain' and not hasattr(self, 'body') or
        content_type == 'text/html' and not hasattr(self, 'html')):

      super(InboundEmailMessage, self)._add_body(content_type, payload)
    else:

      try:
        alternate_bodies = self.alternate_bodies
      except AttributeError:
        alternate_bodies = self.alternate_bodies = [(content_type, payload)]
      else:
        alternate_bodies.append((content_type, payload))

  def bodies(self, content_type: typing.Text = None):
    """Iterates over all bodies.

    Args:
      content_type: Content type on which to filter. This argument allows you to
          select only specific types of content. You can use the base type or
          the content type.

          For example, `content_type = 'text/html'` matches only HTML content,
          and `content_type = 'text'` matches text of any kind.


    Yields:
      A `(content_type, payload)` tuple for all bodies of a message, including
      the body, HTML, and all `alternate_bodies`, in that order.
    """
    main_bodies = super(InboundEmailMessage, self).bodies(content_type)
    for payload_type, payload in main_bodies:
      yield payload_type, payload

    partial_type = bool(content_type and content_type.find('/') < 0)

    try:
      for payload_type, payload in self.alternate_bodies:
        if content_type:
          if partial_type:
            match_type = payload_type.split('/')[0]
          else:
            match_type = payload_type
          match = match_type == content_type
        else:
          match = True

        if match:
          yield payload_type, payload
    except AttributeError:
      pass

  def to_mime_message(self):
    """Converts a message to a MIME message.

    This function adds additional headers from the inbound email.

    Returns:
      The MIME message instance of a payload.
    """
    mime_message = super(InboundEmailMessage, self).to_mime_message()

    for property_, header in six.iteritems(
        InboundEmailMessage.__HEADER_PROPERTIES):
      try:
        mime_message[header] = getattr(self, property_)
      except AttributeError:
        pass

    return mime_message










parser.Parser



class _MultiDict(MutableMapping):
  """A slim version of the WebOb.MultiDict class.

  This only includes functionality needed for accessing POST form vars
  needed for for parsing a BounceNotification object.
  Original WebOb class:
  https://github.com/Pylons/webob/blob/master/src/webob/multidict.py
  """

  def __init__(self):
    self._items = []

  def __len__(self):
    return len(self._items)

  def __getitem__(self, key):
    for k, v in reversed(self._items):
      if k == key:
        return v
    raise KeyError(key)

  def __setitem__(self, key, value):
    try:
      del self[key]
    except KeyError:
      pass
    self._items.append((key, value))

  def __delitem__(self, key):
    items = self._items
    found = False

    for i in range(len(items) - 1, -1, -1):
      if items[i][0] == key:
        del items[i]
        found = True

    if not found:
      raise KeyError(key)

  def add(self, key, value):
    """Add the key and value, not overwriting any previous value."""
    self._items.append((key, value))

  def keys(self):
    for k, _ in self._items:
      yield k

  __iter__ = keys

  @classmethod
  def from_fieldstorage(cls, fs):
    """Create a MultiDict from a cgi.FieldStorage instance.

    This mimics functionality in webob.MultiDict without taking a dependency
    on the WebOb package -
    https://github.com/Pylons/webob/blob/259230aa2b8b9cf675c996e157c5cf021c256059/src/webob/multidict.py#L57

    Args:
      fs: cgi.FieldStorage object correspoinding to a POST request
    Returns:
      MultiDict that contains form variables from the POST request
    """
    obj = cls()


    for field in fs.list or ():
      charset = field.type_options.get('charset', 'utf8')
      transfer_encoding = field.headers.get('Content-Transfer-Encoding', None)
      supported_transfer_encoding = {
          'base64': binascii.a2b_base64,
          'quoted-printable': binascii.a2b_qp,
      }

      if charset == 'utf8':
        def decode(b):
          return b
      else:
        def decode(b):
          return b.encode('utf8').decode(charset)

      if field.filename:
        field.filename = decode(field.filename)
        obj.add(field.name, field)
      else:
        value = field.value

        if transfer_encoding in supported_transfer_encoding:

          value = value.encode('utf8')
          value = supported_transfer_encoding[transfer_encoding](value)


          value = value.decode('utf8')
        obj.add(field.name, decode(value))

    return obj


class BounceNotification(object):
  """Encapsulates a bounce notification received by the application."""

  def __init__(self, post_vars: typing.Mapping[str, typing.Any]):
    """Constructs a new BounceNotification from an HTTP request.

    Properties:
      original: a dict describing the message that caused the bounce.
      notification: a dict describing the bounce itself.
      original_raw_message: the raw message that caused the bounce.

    The 'original' and 'notification' dicts contain the following keys:
      to, cc, bcc, from, subject, text

    Args:
      post_vars: a dictionary with keys as strings. This should
        contain bounce information, and the following keys are handled:
          original-from
          original-to
          original-cc
          original-bcc
          original-subject
          original-text
          notification-from
          notification-to
          notification-cc
          notification-bcc
          notification-subject
          notification-text
          raw-message
        For all keys except 'raw-message', the value can be anything.
        The Bounce Notification object just assigns these values to the
        `original` and `notification` properties of this instance,
        which are dictionaries.
        For example, original["to"] = post_vars.get("original-to")

        The `raw-message` value is used to create an `InboundEmailMessage`
        object. This value should be a valid input to the `EmailMessage`
        constructor (inherited by 'InboundEmailMessage').

        Flask- This is typically the `flask.request.form` field (if
        the user wants to pass single (non-list) values for each key), or
        'dict(flask.request.form.lists())' if the user wants to store a list for
        each key (example use case is multiple `to` and `cc` recipients).

        Webob- `webob.Request.POST` can be used for single values, and
        `webob.Request.POST.dict_of_lists()` for multiple values.

        Django- `request.POST` can be used for single values, and
        `dict(request.POST.lists())` can be used for multiple values.
    """
    self.__original = {}
    self.__notification = {}
    for field in ['to', 'cc', 'bcc', 'from', 'subject', 'text']:
      self.__original[field] = post_vars.get('original-' + field, '')
      self.__notification[field] = post_vars.get('notification-' + field, '')

    raw_message = post_vars.get('raw-message', '')

    if isinstance(raw_message, list):
      if not raw_message:

        raw_message = ''
      elif len(raw_message) > 1:
        raise ValueError('Multiple values found for "raw-message" in post_vars.'
                         ' Expected single value.')
      else:
        raw_message = raw_message[0]

      raw_message = raw_message[0] if raw_message else ''
    self.__original_raw_message = InboundEmailMessage(raw_message)

  @classmethod
  def from_environ(cls, environ):
    """Transforms the HTTP request body to a bounce notification object.

    Example(WSGI)::

      def BounceReceiver(environ, start_response):
        bounce_msg = mail.BounceNotification.from_environ(environ)

        # Add logic for what to do with the bounce notification
        print('Bounce original: %s', bounce_msg.original)
        print('Bounce notification: %s', bounce_msg.notification)

        # Return suitable response
        response = http.HTTPStatus.OK
        start_response(f'{response.value} {response.phrase}', [])
        return ['success'.encode('utf-8')]

    Args:
      environ: a WSGI dict describing the HTTP request (See PEP 333).
    Returns:
      A BounceNotification object.
    """
    fs = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        keep_blank_values=True,
        encoding='utf8',
    )

    post_vars = _MultiDict.from_fieldstorage(fs)
    return BounceNotification(post_vars)

  @property
  def original(self):
    return self.__original

  @property
  def notification(self):
    return self.__notification

  @property
  def original_raw_message(self):
    return self.__original_raw_message
