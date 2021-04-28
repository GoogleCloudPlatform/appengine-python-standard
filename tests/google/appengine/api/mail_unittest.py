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




"""Unit-test for google.appengine.api.mail module"""










import base64
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import zlib

import six
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_types
from google.appengine.api import mail
from google.appengine.api import mail_service_pb2
from google.appengine.api import users
from google.appengine.runtime import apiproxy_errors
from absl.testing import absltest



MIME_MESSAGE_SINGLE_BODY = """\
Received: by 192.168.1.102 with SMTP id s7mr2969ebc.13.1249944077509;
        Mon, 10 Aug 2009 15:41:17 -0700 (PDT)
Return-Path: <nobody@google.com>
Received: from mail-receiver.google.com (mail-receiver.google.com [192.168.1.100])
        by gmr-mx.google.com with ESMTP id 15si1006235ewy.0.2009.08.10.15.41.17;
        Mon, 10 Aug 2009 15:41:17 -0700 (PDT)
Received-SPF: softfail (google.com: domain of transitioning rafek@google.com does not designate 192.168.1.100 as permitted sender) client-ip=192.168.1.100;
Authentication-Results: gmr-mx.google.com; spf=softfail (google.com: domain of transitioning rafek@google.com does not designate 192.168.1.100 as permitted sender) smtp.mail=rafek@google.com
Received: from qw-out-2122.google.com (qwe3.prod.google.com [192.168.1.101])
	by mail-receiver.google.com with ESMTP id n7AMfEPK027033
	for <nobody@hello-mail-nobody.appspot.com>; Mon, 10 Aug 2009 15:41:15 -0700
Received: by qw-out-2122.google.com with SMTP id 3so1282105qwe.29
        for <nobody@hello-mail-nobody.appspot.com>; Mon, 10 Aug 2009 15:41:14 -0700 (PDT)
MIME-Version: 1.0
Received: by 10.229.99.208 with SMTP id blar-blar; Mon, 10 Aug 2009 15:41:14 -0700 (PDT)
Date: Mon, 10 Aug 2009 15:41:14 -0700
Message-ID: <ac02c96f0908101541h77d104caqc78cfbb53b7b9dee@mail.gmail.com>
Subject: A test subject line
From: Google tester <nobody@gmail.com>
To: nobody@google.com
Content-Type: text/plain; charset=ISO-8859-1
Content-Transfer-Encoding: 7bit
X-System-Of-Record: true

This has a body.
"""

MIME_MESSAGE_DUAL_BODY = """\
MIME-Version: 1.0
Received: by 192.168.1.100 with HTTP; Tue, 11 Aug 2009 13:35:56 -0700 (PDT)
Date: Tue, 11 Aug 2009 13:35:56 -0700
Delivered-To: nobody@gmail.com
Message-ID: <ac02c96f0908111335r643ca11bnc6fadd3291eed8a5@mail.gmail.com>
Subject: test dual format
From: Donut <nobody@gmail.com>
To: Donut <nobody@gmail.com>
Content-Type: multipart/alternative; boundary=0016364eed304da2d30470e3a628

--0016364eed304da2d30470e3a628
Content-Type: text/plain; charset=ISO-8859-1
Content-Transfer-Encoding: 7bit

This is *Rich*.

--0016364eed304da2d30470e3a628
Content-Type: text/html; charset=ISO-8859-1
Content-Transfer-Encoding: 7bit

This is <b>Rich</b>.

--0016364eed304da2d30470e3a628--
"""

MIME_MESSAGE_WITH_ATTACHMENT = """\
MIME-Version: 1.0
Received: by 192.168.1.100 with HTTP; Tue, 11 Aug 2009 14:22:21 -0700 (PDT)
Date: Tue, 11 Aug 2009 14:22:21 -0700
Delivered-To: nobody@gmail.com
Message-ID: <ac02c96f0908111422v3c8f3ed5uababde8886a893ed@mail.gmail.com>
Subject: test attachment
From: Donut <nobody@gmail.com>
To: Donut <nobody@gmail.com>
Content-Type: multipart/mixed; boundary=0016360e3dec4b51440470e44c74

--0016360e3dec4b51440470e44c74
Content-Type: multipart/alternative; boundary=0016360e3dec4b513e0470e44c72

--0016360e3dec4b513e0470e44c72
Content-Type: text/plain; charset=ISO-8859-1
Content-Transfer-Encoding: 7bit



--0016360e3dec4b513e0470e44c72
Content-Type: text/html; charset=ISO-8859-1
Content-Transfer-Encoding: 7bit

<br>

--0016360e3dec4b513e0470e44c72--
--0016360e3dec4b51440470e44c74
Content-Type: text/plain; charset=US-ASCII; name="an_attachment.txt"
Content-Disposition: attachment; filename="an_attachment.txt"
Content-Transfer-Encoding: base64
X-Attachment-Id: f_fy951huj0

SSBoYXZlIGRhdGE=
--0016360e3dec4b51440470e44c74--
"""

MIME_MESSAGE_WITH_CONTENT_ID_ATTACHMENT = """\
MIME-Version: 1.0
Received: by 192.168.1.100 with HTTP; Tue, 11 Aug 2009 14:22:21 -0700 (PDT)
Date: Tue, 11 Aug 2009 14:22:21 -0700
Delivered-To: nobody@gmail.com
Message-ID: <ac02c96f0908111422v3c8f3ed5uababde8886a893ed@mail.gmail.com>
Subject: test attachment
From: Donut <nobody@gmail.com>
To: Donut <nobody@gmail.com>
Content-Type: multipart/mixed; boundary=0016360e3dec4b51440470e44c74

--0016360e3dec4b51440470e44c74
Content-Type: multipart/alternative; boundary=0016360e3dec4b513e0470e44c72

--0016360e3dec4b513e0470e44c72
Content-Type: text/plain; charset=ISO-8859-1
Content-Transfer-Encoding: 7bit



--0016360e3dec4b513e0470e44c72
Content-Type: text/html; charset=ISO-8859-1
Content-Transfer-Encoding: 7bit

<br>

--0016360e3dec4b513e0470e44c72--
--0016360e3dec4b51440470e44c74
Content-Type: text/plain; charset=US-ASCII; name="an_attachment.txt"
Content-ID: <attachment>
Content-Disposition: attachment; filename="an_attachment.txt"
Content-Transfer-Encoding: base64
X-Attachment-Id: f_fy951huj0

SSBoYXZlIGRhdGE=
--0016360e3dec4b51440470e44c74--
"""

MIME_MESSAGE_WITH_UNICODE_NAMED_ATTACHMENT = """\
MIME-Version: 1.0
Received: by 192.168.1.100 with HTTP; Tue, 11 Aug 2009 14:22:21 -0700 (PDT)
Date: Tue, 11 Aug 2009 14:22:21 -0700
Delivered-To: nobody@gmail.com
Message-ID: <ac02c96f0908111422v3c8f3ed5uababde8886a893ed@mail.gmail.com>
Subject: test attachment
From: Donut <nobody@gmail.com>
To: Donut <nobody@gmail.com>
Content-Type: multipart/mixed; boundary=0016360e3dec4b51440470e44c74

--0016360e3dec4b51440470e44c74
Content-Type: text/plain; charset=ISO-8859-1
Content-Transfer-Encoding: 7bit

A body.

--0016360e3dec4b51440470e44c74
Content-Type: text/plain; charset=UTF-8; name="GB2312''____.txt"
Content-Disposition: attachment; filename*="GB2312''%D5%D5%C6%AC.txt"
Content-Transfer-Encoding: base64
X-Attachment-Id: f_fy951huj0

SSBoYXZlIGRhdGE=
--0016360e3dec4b51440470e44c74--
"""

MIME_MESSAGE_UNICODE = """\
MIME-Version: 1.0
Received: by 10.229.99.208 with SMTP id blar-blar; Mon, 10 Aug 2009 15:41:14 -0700 (PDT)
Date: Mon, 10 Aug 2009 15:41:14 -0700
Message-ID: <ac02c96f0908101541h77d104caqc78cfbb53b7b9dee@mail.gmail.com>
Subject: =?UTF-8?Q?La_decisi=C3=B3n?=
From: Donut <nobody@gmail.com>
To: Donut <nobody@google.com>
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: quoted-printable

La decisi=C3=B3n ha sido tomada.
"""

MIME_MESSAGE_BLANK_BCC = """\
MIME-Version: 1.0
Date: Mon, 10 Aug 2009 15:41:14 -0700
From: Donut <nobody@gmail.com>
To: xxx@yyyzzz.appspotmail.com
Cc: xxx@xxx.xx
Bcc:
Subject: Issue 4797: Lotus Notes is Strange
X-Mailer: Lotus Notes Release 8.5.1 FP1 January 06, 2010
Content-Type: text/plain

BCC fields with blanks were treated as invalid and never reached user code.
"""

MIME_MESSAGE_RFC_2047_ENCODED_PARTS = """\
MIME-Version: 1.0
Date: Mon, 10 Aug 2009 15:41:14 -0700
From: =?US-ASCII?Q?Keith_Moore?= <moore@cs.utk.edu>
To: =?ISO-8859-1?Q?Keld_J=F8rn_Simonsen?= <keld@dkuug.dk>,
 =?us-ascii?Q?Xxx Yyyzzz?= <xxx@yyyzzz.appspotmail.com>
CC: =?ISO-8859-1?Q?Andr=E9?= Pirard <PIRARD@vm1.ulg.ac.be>, xxx@xxx.xx
Subject: =?ISO-8859-1?B?SWYgeW91IGNhbiByZWFkIHRoaXMgeW8=?=
 =?ISO-8859-2?B?dSB1bmRlcnN0YW5kIHRoZSBleGFtcGxlLg==?=
Content-type: text/plain; charset=ISO-8859-1
Content-Transfer-Encoding: 7bit

This has a body.
"""


class InvalidEmailReasonTest(absltest.TestCase):
  """Tests for invalid_email_reason function."""

  def testValid(self):
    """Test a few valid cases."""
    self.assertTrue(mail.invalid_email_reason('email@nowhere.com',
                                              'arbitrary') is None)
    self.assertTrue(mail.invalid_email_reason('email@sub.nowhere.com',
                                              'arbitrary') is None)
    self.assertTrue(mail.invalid_email_reason('e@sub1.sub2.nowhere.com',
                                              'arbitrary') is None)
    self.assertTrue(mail.invalid_email_reason(
      datastore_types.Email('datastore@nowhere.com'),
      'arbitrary') is None)
    self.assertTrue(mail.invalid_email_reason(
      users.User('user', 'user@nowhere.com'),
      'arbitrary') is None)

    self.assertTrue(mail.InvalidEmailReason('email@nowhere.com',
                                            'arbitrary') is None)

  def testNone(self):
    """Test None case."""
    self.assertEqual('None email address for arbitrary.',
                     mail.invalid_email_reason(None, 'arbitrary'))

  def testEmpty(self):
    """Tests the empty string case."""
    self.assertEqual('Empty email address for arbitrary.',
                     mail.invalid_email_reason('', 'arbitrary'))
    self.assertEqual('Empty email address for arbitrary.',
                     mail.invalid_email_reason('   ', 'arbitrary'))

  def testInvalidType(self):
    """Test invalid email type."""
    self.assertEqual('Invalid email address type for arbitrary.',
                     mail.invalid_email_reason([], 'arbitrary'))
    self.assertEqual('Invalid email address type for arbitrary.',
                     mail.invalid_email_reason(True, 'arbitrary'))


class IsEmailValidTest(absltest.TestCase):
  """Tests is_email_valid function."""

  def testValid(self):
    """Test a few valid cases."""
    self.assertTrue(mail.is_email_valid('email@nowhere.com'))
    self.assertTrue(mail.is_email_valid('email@sub.nowhere.com'))
    self.assertTrue(mail.is_email_valid(u'e@sub1.sub2.nowhere.com'))
    self.assertTrue(mail.is_email_valid(
      datastore_types.Email('datastore@nowhere.com')))
    self.assertTrue(mail.is_email_valid(
      users.User('user', 'user@nowhere.com')))

    self.assertTrue(mail.IsEmailValid('email@nowhere.com'))

  def testInvalid(self):
    """Test a few invalid cases."""
    self.assertFalse(mail.is_email_valid(None))
    self.assertFalse(mail.is_email_valid(''))
    self.assertFalse(mail.is_email_valid('   '))
    self.assertFalse(mail.is_email_valid([]))


class CheckEmailValidTest(absltest.TestCase):
  """Tests check_email_valid function."""

  def testValid(self):
    """Test a few valid cases."""
    mail.check_email_valid('email@nowhere.com', 'arbitrary')
    mail.check_email_valid('email@sub.nowhere.com', 'arbitrary')
    mail.check_email_valid(u'e@sub1.sub2.nowhere.com', 'arbitrary')
    mail.check_email_valid(
      datastore_types.Email('datastore@nowhere.com'),
      'arbitrary')
    mail.check_email_valid(
      users.User('user', 'user@nowhere.com'),
      'arbitrary')

    mail.CheckEmailValid('email@nowhere.com', 'arbitrary')

  def testInvalid(self):
    """Test a few invalid cases."""
    self.assertRaises(mail.InvalidEmailError,
                      mail.check_email_valid, None, 'arbitrary')
    self.assertRaises(mail.InvalidEmailError,
                      mail.check_email_valid, '', 'arbitrary')
    self.assertRaises(mail.InvalidEmailError,
                      mail.check_email_valid, '   ', 'arbitrary')
    self.assertRaises(mail.InvalidEmailError,
                      mail.check_email_valid, [], 'arbitrary')


class InvalidHeadersReasonTest(absltest.TestCase):
  """Tests for invalid_headers_reason."""

  def testValid(self):
    """Test the valid cases."""
    for header in mail.HEADER_WHITELIST:
      self.assertEqual(None, mail.invalid_headers_reason({header: 'value'}))


  def testNone(self):
    """Test None case."""
    self.assertEqual('Headers dictionary was None.',
                     mail.invalid_headers_reason(None))

  def testEmpty(self):
    """Test the empty dict case."""
    self.assertEqual(None, mail.invalid_headers_reason({}))

  def testInvalidType(self):
    """Test invalid headers type."""
    self.assertEqual('Invalid type for headers. Should be a dictionary.',
                     mail.invalid_headers_reason(['list']))
    self.assertEqual('Invalid type for headers. Should be a dictionary.',
                     mail.invalid_headers_reason('string'))
    self.assertEqual('Header names should be strings.',
                     mail.invalid_headers_reason({123: 'value'}))
    self.assertEqual('Header values should be strings.',
                     mail.invalid_headers_reason({'header': True}))
    self.assertEqual('Header values should be strings.',
                     mail.invalid_headers_reason({'header': 1235}))
    self.assertEqual('Header values should be strings.',
                     mail.invalid_headers_reason({'header': ['value']}))
    self.assertEqual('Header "Invalid-Name" is not allowed.',
                     mail.invalid_headers_reason({'Invalid-Name': ''}))
    unicode_value = u'\u05cb'
    utf_8_header = '%s-Header' % unicode_value
    self.assertEqual('Header name should be an ASCII string.',
                     mail.invalid_headers_reason({utf_8_header: 'value'}))


class TestEmailMessageToMIMEMessage(absltest.TestCase):
  """Tests the MailMessageToMIMEMessage function."""

  def testEmailMessageToMIMEMessage(self):
    """Tests conversion of MailMessage to MIME message."""
    attachments = [('html.html', 'html1'), ('txt.txt', 'txt1'),
                   mail.Attachment('sub.dir/jpeg.jpg', 'jpg1'),
                   mail.Attachment(
                       'image.jpg',
                       mail.EncodedPayload(b'image data'),
                       content_id='<image>')]
    message = mail.EmailMessage(sender='from@nowhere.com',
                                to=['to1@nowhere.com',
                                    'to2@nowhere.com'],
                                subject='a subject',
                                body='a body',
                                html='<html>',
                                cc=['cc1@nowhere.com',
                                    'cc2@nowhere.com'],
                                bcc=['bcc1@nowhere.com',
                                     'bcc2@nowhere.com'],
                                reply_to='replyto@nowhere.com',
                                attachments=attachments)

    mime_message = mail.MailMessageToMIMEMessage(message.ToProto())

    self.assertEqual(
        {
            'To': 'to1@nowhere.com, to2@nowhere.com',
            'Cc': 'cc1@nowhere.com, cc2@nowhere.com',
            'Bcc': 'bcc1@nowhere.com, bcc2@nowhere.com',
            'Reply-To': 'replyto@nowhere.com',
            'Subject': 'a subject',
            'From': 'from@nowhere.com',
            'Content-Type': 'multipart/mixed',
            'MIME-Version': '1.0'
        }, dict(list(mime_message.items())))

    (bodies,
     html_attachment,
     text_attachment,
     jpg_attachment,
     content_id_attachment) = mime_message.get_payload()
    self.assertEqual('text/html', html_attachment.get_content_type())
    self.assertEqual('html1', html_attachment.get_payload())
    self.assertEqual('text/plain', text_attachment.get_content_type())
    self.assertEqual('txt1', text_attachment.get_payload())
    self.assertEqual('image/jpeg', jpg_attachment.get_content_type())
    self.assertEqual('jpg1', jpg_attachment.get_payload())
    self.assertIn('content-id', content_id_attachment)

    body, html = bodies.get_payload()
    self.assertEqual('text/plain', body.get_content_type())
    self.assertEqual('a body', body.get_payload())
    self.assertEqual('text/html', html.get_content_type())
    self.assertEqual('<html>', html.get_payload())

  def testEmailMessageToMIMEMessageWithReferences(self):
    """Tests conversion of MailMessage to MIME message."""
    message = mail.EmailMessage(sender='from@nowhere.com',
                                to=['to1@nowhere.com',
                                    'to2@nowhere.com'],
                                subject='a subject',
                                body='a body',
                                html='<html>',
                                cc=['cc1@nowhere.com',
                                    'cc2@nowhere.com'],
                                bcc=['bcc1@nowhere.com',
                                     'bcc2@nowhere.com'],
                                reply_to='replyto@nowhere.com',
                                headers={'In-Reply-To': 'asdf',
                                         'List-Id': 'some-list',
                                         'References': 'qwerty'},
                                attachments=[('html.html',
                                              'html1'),
                                             ('txt.txt',
                                              'txt1'),
                                             ('sub.dir/jpeg.jpg',
                                              'jpg1')])

    mime_message = mail.MailMessageToMIMEMessage(message.ToProto())

    self.assertEqual(
        {
            'To': 'to1@nowhere.com, to2@nowhere.com',
            'Cc': 'cc1@nowhere.com, cc2@nowhere.com',
            'Bcc': 'bcc1@nowhere.com, bcc2@nowhere.com',
            'Reply-To': 'replyto@nowhere.com',
            'Subject': 'a subject',
            'From': 'from@nowhere.com',
            'In-Reply-To': 'asdf',
            'List-Id': 'some-list',
            'References': 'qwerty',
            'Content-Type': 'multipart/mixed',
            'MIME-Version': '1.0'
        }, dict(list(mime_message.items())))

    bodies, html_attachment, text_attachment, jpg_attachment = (
            mime_message.get_payload())
    self.assertEqual('text/html', html_attachment.get_content_type())
    self.assertEqual('html1', html_attachment.get_payload())
    self.assertEqual('text/plain', text_attachment.get_content_type())
    self.assertEqual('txt1', text_attachment.get_payload())
    self.assertEqual('image/jpeg', jpg_attachment.get_content_type())
    self.assertEqual('jpg1', jpg_attachment.get_payload())

    body, html = bodies.get_payload()
    self.assertEqual('text/plain', body.get_content_type())
    self.assertEqual('a body', body.get_payload())
    self.assertEqual('text/html', html.get_content_type())
    self.assertEqual('<html>', html.get_payload())

  def testEmailMessageToMIMEMessageInvalidEmail(self):
    """Tests invalid email attachments."""
    message = mail.EmailMessage(sender='from@nowhere.com',
                                to=['to1@nowhere.com'],
                                subject='a subject',
                                body='a body',
                                attachments=[('html.html',
                                              'html1')])


    message_proto = message.ToProto()
    message_proto.Attachment[0].FileName = 'OLDVIRUS.COM'

    self.assertRaises(mail.InvalidAttachmentTypeError,
                      mail.MailMessageToMIMEMessage,
                      message_proto)

    message_proto = message.ToProto()
    message_proto.Attachment[0].FileName = 'myvirus.exe'

    self.assertRaises(mail.InvalidAttachmentTypeError,
                      mail.MailMessageToMIMEMessage,
                      message_proto)

  def testAdminEmailMessageToMIMEMessage(self):
    """Tests conversion of MailMessage to MIME message."""
    message = mail.AdminEmailMessage(sender='from@nowhere.com',
                                     subject='a subject',
                                     body='a body',
                                     html='<html>',
                                     reply_to='replyto@nowhere.com',
                                     attachments=[('html.html',
                                                   'html1'),
                                                  ('txt.txt',
                                                   'txt1'),
                                                  ('sub.dir/jpeg.jpg',
                                                   'jpg1')])

    mime_message = mail.MailMessageToMIMEMessage(message.ToProto())

    self.assertEqual(
        {
            'Reply-To': 'replyto@nowhere.com',
            'Subject': 'a subject',
            'From': 'from@nowhere.com',
            'Content-Type': 'multipart/mixed',
            'MIME-Version': '1.0'
        }, dict(list(mime_message.items())))

    bodies, html_attachment, text_attachment, jpg_attachment = (
        mime_message.get_payload())
    self.assertEqual('text/html', html_attachment.get_content_type())
    self.assertEqual('html1', html_attachment.get_payload())
    self.assertEqual('text/plain', text_attachment.get_content_type())
    self.assertEqual('txt1', text_attachment.get_payload())
    self.assertEqual('image/jpeg', jpg_attachment.get_content_type())
    self.assertEqual('jpg1', jpg_attachment.get_payload())

    body, html = bodies.get_payload()
    self.assertEqual('text/plain', body.get_content_type())
    self.assertEqual('a body', body.get_payload())
    self.assertEqual('text/html', html.get_content_type())
    self.assertEqual('<html>', html.get_payload())


class EmailMessageTest(absltest.TestCase):
  """Test EmailMessage class."""

  def setUp(self):
    """Sets up fixture with email message instance."""
    self.message = mail.EmailMessage()
    self.admin_message = mail.AdminEmailMessage()

  def DoEmailAttributeTest(self, attribute):
    """Do generic single email attribute test.

    Used for testing fields which require a single email address.

    Args:
      attribute: Name of email field to test.
    """

    setattr(self.message, attribute, 'email@nowhere.com')
    self.assertEqual('email@nowhere.com', getattr(self.message, attribute))
    delattr(self.message, attribute)
    self.assertFalse(hasattr(self.message, attribute))


    self.assertRaises(mail.InvalidEmailError, setattr, self.message, attribute,
                      '')
    self.assertRaises(mail.InvalidEmailError, setattr, self.message, attribute,
                      None)
    self.assertRaises(mail.InvalidEmailError, setattr, self.message, attribute,
                      [])

  def DoEmailListAttributeTest(self, attribute):
    """Do generic multiple email attribute test.

    Used for test fields which can accept multiple email addresses.

    Args:
      attribute: Name of attribute to test.
    """

    setattr(self.message, attribute, 'email@nowhere.com')
    self.assertEqual('email@nowhere.com', getattr(self.message, attribute))
    setattr(self.message, attribute, ('email1@nowhere.com', 'email2@nowhere.com'))
    self.assertEqual(('email1@nowhere.com', 'email2@nowhere.com'),
                     getattr(self.message, attribute))
    delattr(self.message, attribute)
    self.assertFalse(hasattr(self.message, attribute))


    self.assertRaises(mail.InvalidEmailError, setattr, self.message, attribute,
                      ('email@nowhere.com', None))

  def testInitializedState(self):
    """Test to make sure all variables unset after construction."""
    for message in (self.message, self.admin_message):
      self.assertFalse(message.is_initialized())
      for attribute in message.PROPERTIES:
        self.assertFalse(hasattr(message, attribute))

  def testSubject(self):
    """Test subject field"""
    self.message.subject = 'subject'
    self.assertEqual('subject', self.message.subject)
    del self.message.subject
    self.assertFalse(hasattr(self.message, 'subject'))

  def testMissingSender(self):
    """Make sure message is uninitialized without 'sender'"""
    self.message.to = ['to@nowhere.com']
    self.message.subject = 'subject'
    self.message.body = 'body'
    self.assertFalse(self.message.is_initialized())

  def testMissingRecipients(self):
    """Make sure message is uninitialized without 'to'"""
    self.message.sender = 'sender@nowhere.com'
    self.message.subject = 'subject'
    self.message.body = 'body'
    self.assertFalse(self.message.is_initialized())

  def testMissingRecipientsDoesNotMatterToAdminEmail(self):
    """Make sure message admin email ignores recipients"""
    self.admin_message.sender = 'sender@nowhere.com'
    self.admin_message.to = 'whatever@nowhere.com'
    self.admin_message.subject = 'subject'
    self.admin_message.body = 'body'
    self.assertTrue(self.admin_message.is_initialized())

  def testMissingBody(self):
    """Make sure message is initialized without bodies"""
    self.message.sender = 'sender@nowhere.com'
    self.message.subject = 'subject'
    self.message.to = ['someone@nowhere.com']
    self.assertTrue(self.message.is_initialized())

  def testHasCc(self):
    """Make sure message is initialized with 'cc'"""
    self.message.sender = 'sender@nowhere.com'
    self.message.cc = ['someone@nowhere.com']
    self.message.subject = 'subject'
    self.message.body = 'body'
    self.message.check_initialized()

  def testHasBcc(self):
    """Make sure message is initialized with 'bcc'"""
    self.message.sender = 'sender@nowhere.com'
    self.message.bcc = ['someone@nowhere.com']
    self.message.subject = 'subject'
    self.message.body = 'body'
    self.message.check_initialized()

  def testHasHtmlBody(self):
    """Make sure initialization occurs when sender, to, subject and body set."""
    self.message.sender = 'sender@nowhere.com'
    self.message.to = ['someone@nowhere.com']
    self.message.subject = 'subject'
    self.message.html = 'body'
    self.message.check_initialized()

  def testAttachmentsFieldError(self):
    """Check attachment errors."""
    self.message.sender = 'sender@nowhere.com'
    self.message.to = ['someone@nowhere.com']
    self.message.subject = 'subject'
    self.message.body = 'body'

    self.message.attachments = ('file.exe', 'Windows virus')
    self.assertRaises(mail.InvalidAttachmentTypeError,
                      self.message.check_initialized)

  def testCaseInsensitiveAttachments(self):
    """Check that attachments filters are case insensitive."""
    mail._GetMimeType('file.TXT')
    mail._GetMimeType('page.HTMl')
    mail._GetMimeType('file.tXt')

  def testAttachmentDecodeError(self):
    self.message.sender = 'sender@nowhere.com'
    self.message.to = ['someone@nowhere.com']
    self.message.subject = 'subject'
    self.message.body = 'body'

    self.message.attachments = ('unknown.png',
                                mail.EncodedPayload(
                                    b'unknown', encoding='weird_encoding'))
    self.assertRaises(mail.UnknownEncodingError,
                      self.message.check_initialized)

    self.message.attachments = ('unknown.png',
                                mail.EncodedPayload(b'unknown',
                                                    'weird_charset'))
    self.assertRaises(mail.UnknownCharsetError,
                      self.message.check_initialized)

    self.message.attachments = ('unknown.png',
                                mail.EncodedPayload(
                                    b'bad data', encoding='base64'))
    self.assertRaises(mail.PayloadEncodingError,
                      self.message.check_initialized)

    self.message.attachments = ('unknown.png',
                                mail.EncodedPayload(b'\x80', 'ascii'))
    self.assertRaises(mail.PayloadEncodingError,
                      self.message.check_initialized)

  def testBodyDecodeError(self):
    self.message.sender = 'sender@nowhere.com'
    self.message.to = ['someone@nowhere.com']
    self.message.subject = 'subject'

    for attribute in 'body', 'html':
      self.message.body = 'body'
      self.message.html = 'html'

      setattr(self.message, attribute,
              mail.EncodedPayload(b'unknown', encoding='weird_encoding'))
      self.assertRaises(mail.UnknownEncodingError,
                        self.message.check_initialized)

      setattr(self.message, attribute,
              mail.EncodedPayload(b'unknown', 'weird_charset'))
      self.assertRaises(mail.UnknownCharsetError,
                        self.message.check_initialized)

      setattr(self.message, attribute,
              mail.EncodedPayload(b'bad data', encoding='base64'))
      self.assertRaises(mail.PayloadEncodingError,
                        self.message.check_initialized)

      setattr(self.message, attribute, mail.EncodedPayload(b'\x80', 'ascii'))
      self.assertRaises(mail.PayloadEncodingError,
                        self.message.check_initialized)

  def testBodyDecode(self):
    self.assertEqual(
        b'decisi\xc3\xb3n',
        mail.EncodedPayload(b'decisi=C3=B3n',
                            encoding='quoted-printable').decode())

    self.assertEqual(
        u'decisi\xf3n',
        mail.EncodedPayload(b'decisi\xc3\xb3n', charset='UTF-8').decode())

    self.assertEqual(
        u'decisi\xf3n',
        mail.EncodedPayload(
            b'decisi=C3=B3n', charset='UTF-8',
            encoding='quoted-printable').decode())

  def testAddressFields(self):
    """Test address fields."""
    for attribute in ('sender', 'reply_to'):
      self.DoEmailAttributeTest(attribute)

  def testAddressListFields(self):
    """Test address list fields."""
    for attribute in ('to', 'cc', 'bcc'):
      self.DoEmailListAttributeTest(attribute)

  def testTextBodyField(self):
    """Test text body field."""
    self.message.body = 'body'
    self.assertEqual('body', self.message.body)
    del self.message.body
    self.assertFalse(hasattr(self.message, 'body'))

  def testHtmlBodyField(self):
    """Test html body field."""
    self.message.html = 'html'
    self.assertEqual('html', self.message.html)
    del self.message.html
    self.assertFalse(hasattr(self.message, 'html'))

  def testAttachmentField(self):
    """Test attachment field."""
    self.message.attachments = ('file.html', '<body>')
    self.assertEqual(('file.html', '<body>'), self.message.attachments)

    self.message.attachments = (('file1.html', '<body>'),
                                ('file2.txt', 'body'))
    self.assertEqual((('file1.html', '<body>'), ('file2.txt', 'body')),
                     self.message.attachments)
    del self.message.attachments
    self.assertFalse(hasattr(self.message, 'attachments'))

  def testHeadersField(self):

    setattr(self.message, 'headers', {'References': 'value'})
    self.assertEqual({'References': 'value'}, getattr(self.message, 'headers'))
    delattr(self.message, 'headers')
    self.assertFalse(hasattr(self.message, 'headers'))


    self.assertRaises(mail.InvalidEmailError, setattr, self.message, 'headers',
                      '')
    self.assertRaises(mail.InvalidEmailError, setattr, self.message, 'headers',
                      None)
    self.assertRaises(mail.InvalidEmailError, setattr, self.message, 'headers',
                      [])
    self.assertRaises(mail.InvalidEmailError, setattr, self.message, 'headers',
                      {4512: 'value'})
    self.assertRaises(mail.InvalidEmailError, setattr, self.message, 'headers',
                      {'header': False})

  def testKeywords(self):
    """Test keywords sent to the constructor."""
    message = mail.EmailMessage(sender='from@nowhere.com',
                                to=['to@nowhere.com'],
                                subject='subject',
                                body='body',
                                html='<body>',
                                reply_to='reply@nowhere.com',
                                cc=['cc@nowhere.com'],
                                bcc=['bcc@nowhere.com'],
                                attachments=('h.html', '<h>'))
    self.assertEqual('from@nowhere.com', message.sender)
    self.assertEqual(['to@nowhere.com'], message.to)
    self.assertEqual('subject', message.subject)
    self.assertEqual('body', message.body)
    self.assertEqual('<body>', message.html)
    self.assertEqual('reply@nowhere.com', message.reply_to)
    self.assertEqual(['cc@nowhere.com'], message.cc)
    self.assertEqual(['bcc@nowhere.com'], message.bcc)
    self.assertEqual(('h.html', '<h>'), message.attachments)


    self.assertRaises(AttributeError, mail.EmailMessage, no_keyword='value')

  def testToProtoBasic(self):
    """Test conversion of minimum fields to PB."""
    message = mail.EmailMessage(sender='from@nowhere.com',
                                to=['to@nowhere.com'],
                                subject='subject',
                                body='body').ToProto()

    self.assertEqual('from@nowhere.com', message.Sender)
    self.assertLen(message.To, 1)
    self.assertEqual('to@nowhere.com', message.To[0])
    self.assertEqual('subject', message.Subject)
    self.assertEqual('body', message.TextBody)
    self.assertFalse(message.HasField('ReplyTo'))
    self.assertEmpty(message.Cc)
    self.assertEmpty(message.Bcc)
    self.assertEmpty(message.Attachment)

  def testToProtoBasicAdmin(self):
    """Test conversion of minimum admin fields to PB."""
    message = mail.AdminEmailMessage(sender='from@nowhere.com',
                                     subject='subject',
                                     body='body',
                                     to='Just another prop, ignored').ToProto()

    self.assertEqual('from@nowhere.com', message.Sender)
    self.assertEmpty(message.To)
    self.assertEqual('subject', message.Subject)
    self.assertEqual('body', message.TextBody)
    self.assertFalse(message.HasField('ReplyTo'))
    self.assertEmpty(message.Cc)
    self.assertEmpty(message.Bcc)
    self.assertEmpty(message.Attachment)

  def testToProtoFull(self):
    """Test all fields conversions on EmailMessage."""
    message = mail.EmailMessage(sender='from@nowhere.com',
                                to=['to@nowhere.com', 'anotherto@nowhere.com'],
                                subject='subject',
                                body='body',
                                reply_to='reply@nowhere.com',
                                cc=['cc@nowhere.com', 'anothercc@nowhere.com'],
                                bcc=['bcc@nowhere.com',
                                     'anotherbcc@nowhere.com'],
                                attachments=[
                                    ('text.txt', 'text'),
                                    mail.Attachment('foo.jpg',
                                                    'data',
                                                    content_id='<image>')],
                                headers={'In-Reply-To': '<msg>',
                                         'List-Id': 'some-list',
                                         'References': '<msg_id>'}).ToProto()

    self.assertEqual('from@nowhere.com', message.Sender)
    self.assertEqual(2, len(message.To))
    self.assertEqual('to@nowhere.com', message.To[0])
    self.assertEqual('anotherto@nowhere.com', message.To[1])
    self.assertEqual('subject', message.Subject)
    self.assertEqual('body', message.TextBody)
    self.assertEqual('reply@nowhere.com', message.ReplyTo)
    self.assertEqual(2, len(message.Cc))
    self.assertEqual('cc@nowhere.com', message.Cc[0])
    self.assertEqual('anothercc@nowhere.com', message.Cc[1])
    self.assertEqual(2, len(message.Bcc))
    self.assertEqual('bcc@nowhere.com', message.Bcc[0])
    self.assertEqual('anotherbcc@nowhere.com', message.Bcc[1])
    self.assertEqual(2, len(message.Attachment))
    self.assertEqual('text.txt', message.Attachment[0].FileName)
    self.assertEqual(b'text', message.Attachment[0].Data)
    self.assertEqual('foo.jpg', message.Attachment[1].FileName)
    self.assertEqual(b'data', message.Attachment[1].Data)
    self.assertEqual('<image>', message.Attachment[1].ContentID)
    headers = dict([(header.name, header.value) for header in message.Header])
    self.assertEqual(headers, {'In-Reply-To': '<msg>',
                               'List-Id': 'some-list',
                               'References': '<msg_id>'})

  def testToProtoFullSingleItems(self):
    """Test all fields conversions on EmailMessage with non list recipients."""
    message = mail.EmailMessage(sender='from@nowhere.com',
                                to='to@nowhere.com',
                                subject='subject',
                                body='body',
                                reply_to='reply@nowhere.com',
                                cc='cc@nowhere.com',
                                bcc='bcc@nowhere.com',
                                attachments=('text.txt', 'text')).ToProto()

    self.assertEqual('from@nowhere.com', message.Sender)
    self.assertLen(message.To, 1)
    self.assertEqual('to@nowhere.com', message.To[0])
    self.assertEqual('subject', message.Subject)
    self.assertEqual('body', message.TextBody)
    self.assertEqual('reply@nowhere.com', message.ReplyTo)
    self.assertLen(message.Cc, 1)
    self.assertEqual('cc@nowhere.com', message.Cc[0])
    self.assertLen(message.Bcc, 1)
    self.assertEqual('bcc@nowhere.com', message.Bcc[0])
    self.assertLen(message.Attachment, 1)
    self.assertEqual('text.txt', message.Attachment[0].FileName)
    self.assertEqual(b'text', message.Attachment[0].Data)

  def testToProtoFullSingleItemsWithCommaSeparatedList(self):
    """Test all fields conversions on EmailMessage with CSV recipients."""
    message = mail.EmailMessage(sender='from@nowhere.com',
                                to='to@nowhere.com, anotherto@nowhere.com',
                                subject='subject',
                                body='body',
                                reply_to='reply@nowhere.com',
                                cc='cc@nowhere.com, anothercc@nowhere.com',
                                bcc='bcc@nowhere.com, anotherbcc@nowhere.com',
                                attachments=('text.txt', 'text')).ToProto()

    self.assertEqual('from@nowhere.com', message.Sender)
    self.assertEqual(2, len(message.To))
    self.assertEqual('to@nowhere.com', message.To[0])
    self.assertEqual('anotherto@nowhere.com', message.To[1])
    self.assertEqual('subject', message.Subject)
    self.assertEqual('body', message.TextBody)
    self.assertEqual('reply@nowhere.com', message.ReplyTo)
    self.assertEqual(2, len(message.Cc))
    self.assertEqual('cc@nowhere.com', message.Cc[0])
    self.assertEqual('anothercc@nowhere.com', message.Cc[1])
    self.assertEqual(2, len(message.Bcc))
    self.assertEqual('bcc@nowhere.com', message.Bcc[0])
    self.assertEqual('anotherbcc@nowhere.com', message.Bcc[1])
    self.assertEqual(1, len(message.Attachment))
    self.assertEqual('text.txt', message.Attachment[0].FileName)
    self.assertEqual(b'text', message.Attachment[0].Data)

  def testEmailMessageToMIMEMessage(self):
    """Tests conversion of EmailMessage to MIME message."""
    message = mail.EmailMessage(sender='from@nowhere.com',
                                to=['to1@nowhere.com',
                                    'to2@nowhere.com'],
                                subject='a subject',
                                body='a body',
                                html='<html>',
                                cc=['cc1@nowhere.com',
                                    'cc2@nowhere.com'],
                                bcc=['bcc1@nowhere.com',
                                     'bcc2@nowhere.com'],
                                reply_to='replyto@nowhere.com',
                                attachments=[('html.html',
                                              'html1'),
                                             ('txt.txt',
                                              'txt1')])

    mime_message = message.ToMIMEMessage()

    self.assertEqual(
        {
            'To': 'to1@nowhere.com, to2@nowhere.com',
            'Cc': 'cc1@nowhere.com, cc2@nowhere.com',
            'Bcc': 'bcc1@nowhere.com, bcc2@nowhere.com',
            'Reply-To': 'replyto@nowhere.com',
            'Subject': 'a subject',
            'From': 'from@nowhere.com',
            'Content-Type': 'multipart/mixed',
            'MIME-Version': '1.0'
        }, dict(list(mime_message.items())))

    bodies, html_attachment, text_attachment = mime_message.get_payload()
    self.assertEqual('html.html', html_attachment.get_filename())
    self.assertEqual('text/html', html_attachment.get_content_type())
    self.assertEqual('html1', html_attachment.get_payload())
    self.assertEqual('txt.txt', text_attachment.get_filename())
    self.assertEqual('text/plain', text_attachment.get_content_type())
    self.assertEqual('txt1', text_attachment.get_payload())

    body, html = bodies.get_payload()
    self.assertEqual('text/plain', body.get_content_type())
    self.assertEqual('a body', body.get_payload())
    self.assertEqual('text/html', html.get_content_type())
    self.assertEqual('<html>', html.get_payload())

  def testAdminEmailMessageToMIMEMessage(self):
    """Tests conversion of AdminEmailMessage to MIME message."""
    message = mail.AdminEmailMessage(sender='from@nowhere.com',
                                     subject='a subject',
                                     body='a body',
                                     html='<html>',
                                     reply_to='replyto@nowhere.com',
                                     attachments=[('html.html',
                                                   'html1'),
                                                  ('txt.txt',
                                                   'txt1')])

    mime_message = message.ToMIMEMessage()

    self.assertEqual(
        {
            'Reply-To': 'replyto@nowhere.com',
            'Subject': 'a subject',
            'From': 'from@nowhere.com',
            'Content-Type': 'multipart/mixed',
            'MIME-Version': '1.0'
        }, dict(list(mime_message.items())))

    bodies, html_attachment, text_attachment = mime_message.get_payload()
    self.assertEqual('html.html', html_attachment.get_filename())
    self.assertEqual('text/html', html_attachment.get_content_type())
    self.assertEqual('html1', html_attachment.get_payload())
    self.assertEqual('txt.txt', text_attachment.get_filename())
    self.assertEqual('text/plain', text_attachment.get_content_type())
    self.assertEqual('txt1', text_attachment.get_payload())

    body, html = bodies.get_payload()
    self.assertEqual('text/plain', body.get_content_type())
    self.assertEqual('a body', body.get_payload())
    self.assertEqual('text/html', html.get_content_type())
    self.assertEqual('<html>', html.get_payload())

  def testEmailMessageUnicode(self):
    """Tests that all fields of an email message works with unicode."""
    unicode_value = u'\u05cb'
    utf_8_value = unicode_value.encode('utf-8')

    message = mail.EmailMessage(
        sender=unicode_value + '_sender@nowhere.com',
        reply_to=unicode_value + '_reply_to@nowhere.com',
        to=unicode_value + '_to@nowhere.com',
        cc=unicode_value + '_cc@nowhere.com',
        bcc=unicode_value + '_bcc@nowhere.com',
        subject=unicode_value,
        body=unicode_value,
        html=unicode_value,
        attachments=[(unicode_value + u'.txt', unicode_value)],
        headers={'In-Reply-To': unicode_value + '_canBeUTF8'}
        )
    proto = message.ToProto()

    self.assertEqual(unicode_value + '_sender@nowhere.com', proto.Sender)
    self.assertEqual(unicode_value + '_to@nowhere.com', proto.To[0])
    self.assertEqual(unicode_value + '_cc@nowhere.com', proto.Cc[0])
    self.assertEqual(unicode_value + '_bcc@nowhere.com', proto.Bcc[0])
    self.assertEqual(unicode_value, proto.Subject)
    self.assertEqual(unicode_value, proto.TextBody)
    self.assertEqual(unicode_value, proto.HtmlBody)
    self.assertEqual(unicode_value + '.txt', proto.Attachment[0].FileName)
    self.assertEqual(utf_8_value, proto.Attachment[0].Data)
    self.assertEqual(unicode_value + '_canBeUTF8', proto.Header[0].value)





  def testSetFromMimeMessage(self):
    """Test converting from mime-message to instance of email class."""

    for base_class in (mail._EmailMessageBase,
                       mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      calls = []
      class SomeEmailClass(base_class):

        test = self

        def update_from_mime_message(self, mime_message):
          self.test.assertTrue(isinstance(mime_message, email.message.Message))
          calls.append(mime_message.as_string())
          super(SomeEmailClass, self).update_from_mime_message(mime_message)

      EMAIL_MESSAGE = ('From: nobody@nowhere.com\n'
                       'To: another@nowhere.com\n'
                       '\n'
                       'a mime message\n')


      instance = SomeEmailClass(EMAIL_MESSAGE)
      self.assertEqual([EMAIL_MESSAGE], calls)
      self.assertEqual('nobody@nowhere.com', instance.sender)
      self.assertTrue(EMAIL_MESSAGE, instance.original.as_string())

      calls = []

  def testParametersTakePrecedence(self):
    message = mail.AdminEmailMessage('From: nobody@nowhere.com\n\nHello',
                                     sender='admin@nowhere.com')

    self.assertEqual('admin@nowhere.com', message.sender)

  def testUpdateFromMimeMessage_NoFields(self):
    for mail_class in (mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      mime_message = email.message.Message()
      admin_email = mail_class()
      admin_email.update_from_mime_message(mime_message)

      self.assertFalse(hasattr(admin_email, 'sender'))
      self.assertFalse(hasattr(admin_email, 'reply_to'))
      self.assertFalse(hasattr(admin_email, 'subject'))
      self.assertFalse(hasattr(admin_email, 'body'))
      self.assertFalse(hasattr(admin_email, 'html'))
      self.assertFalse(hasattr(admin_email, 'attachments'))

  def testUpdateFromMimeMessage_SingleBody(self):
    for mail_class in (mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      mime_message = email.message_from_string(MIME_MESSAGE_SINGLE_BODY)
      admin_email = mail_class()
      admin_email.update_from_mime_message(mime_message)

      self.assertEqual('Google tester <nobody@gmail.com>', admin_email.sender)
      self.assertEqual('A test subject line', admin_email.subject)
      self.assertEqual(
          mail.EncodedPayload(
              b'This has a body.\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.body)
      self.assertFalse(hasattr(admin_email, 'html'))
      self.assertFalse(hasattr(admin_email, 'attachments'))

  def testUpdateFromMimeMessage_DualBody(self):
    for mail_class in (mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      mime_message = email.message_from_string(MIME_MESSAGE_DUAL_BODY)
      admin_email = mail_class()
      admin_email.update_from_mime_message(mime_message)

      self.assertEqual('Donut <nobody@gmail.com>', admin_email.sender)
      self.assertEqual('test dual format', admin_email.subject)
      self.assertEqual(
          mail.EncodedPayload(
              b'This is *Rich*.\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.body)
      self.assertEqual(
          mail.EncodedPayload(
              b'This is <b>Rich</b>.\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.html)
      self.assertFalse(hasattr(admin_email, 'attachments'))

  def testUpdateFromMimeMessage_Unicode(self):
    for mail_class in (mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      mime_message = email.message_from_string(MIME_MESSAGE_UNICODE)
      admin_email = mail_class()
      admin_email.update_from_mime_message(mime_message)

      self.assertEqual('Donut <nobody@gmail.com>', admin_email.sender)


      self.assertEqual(u'La decisi\xf3n', admin_email.subject)
      self.assertEqual(
          mail.EncodedPayload(
              b'La decisi=C3=B3n ha sido tomada.\n',
              encoding='quoted-printable',
              charset='utf-8'), admin_email.body)
      self.assertFalse(hasattr(admin_email, 'html'))
      self.assertFalse(hasattr(admin_email, 'attachments'))

  def testUpdateFromMimeMessage_WithUnicodeNamedAttachment(self):
    for mail_class in (mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      mime_message = email.message_from_string(
          MIME_MESSAGE_WITH_UNICODE_NAMED_ATTACHMENT)
      admin_email = mail_class()
      admin_email.update_from_mime_message(mime_message)

      self.assertEqual('Donut <nobody@gmail.com>', admin_email.sender)
      self.assertEqual('test attachment', admin_email.subject)
      self.assertEqual(
          mail.EncodedPayload(
              b'A body.\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.body)
      self.assertTrue(hasattr(admin_email, 'attachments'))
      self.assertEqual(
          [(u'\u7167\u7247.txt',
            mail.EncodedPayload(b'SSBoYXZlIGRhdGE=', 'utf-8', 'base64'))],
          admin_email.attachments)

  def testUpdateFromMimeMessage_WithAttachment(self):
    for mail_class in (mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      mime_message = email.message_from_string(MIME_MESSAGE_WITH_ATTACHMENT)
      admin_email = mail_class()
      admin_email.update_from_mime_message(mime_message)

      self.assertEqual('Donut <nobody@gmail.com>', admin_email.sender)
      self.assertEqual('test attachment', admin_email.subject)
      self.assertEqual(
          mail.EncodedPayload(b'\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.body)
      self.assertEqual(
          mail.EncodedPayload(b'<br>\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.html)
      self.assertTrue(hasattr(admin_email, 'attachments'))
      self.assertEqual(
          [('an_attachment.txt',
            mail.EncodedPayload(b'SSBoYXZlIGRhdGE=', 'us-ascii', 'base64'))],
          admin_email.attachments)

  def testUpdateFromMimeMessage_WithAttachmentContentID(self):
    for mail_class in (mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      mime_message = email.message_from_string(
          MIME_MESSAGE_WITH_CONTENT_ID_ATTACHMENT)
      admin_email = mail_class()
      admin_email.update_from_mime_message(mime_message)

      self.assertEqual('Donut <nobody@gmail.com>', admin_email.sender)
      self.assertEqual('test attachment', admin_email.subject)
      self.assertEqual(
          mail.EncodedPayload(b'\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.body)
      self.assertEqual(
          mail.EncodedPayload(b'<br>\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.html)
      self.assertTrue(hasattr(admin_email, 'attachments'))
      self.assertEqual([('an_attachment.txt',
                         mail.EncodedPayload(b'SSBoYXZlIGRhdGE=', 'us-ascii',
                                             'base64'), '<attachment>')],
                       admin_email.attachments)

  def testUpdateFromMimeMessage_NewAttachment(self):
    """Test updating from mime message adding an attachment to singleton list.

    User code may add an attachment as a simple tuple.  In this case, need to
    ensure that when more attachments are added via updating from a mime message
    the old tuple is handled correctly.
    """
    for mail_class in (mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      mime_message = email.message_from_string(MIME_MESSAGE_WITH_ATTACHMENT)
      admin_email = mail_class()
      admin_email.attachments = ('original.txt', 'stuff')
      admin_email.update_from_mime_message(mime_message)

      self.assertEqual('Donut <nobody@gmail.com>', admin_email.sender)
      self.assertEqual('test attachment', admin_email.subject)
      self.assertEqual(
          mail.EncodedPayload(b'\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.body)
      self.assertEqual(
          mail.EncodedPayload(b'<br>\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.html)
      self.assertTrue(hasattr(admin_email, 'attachments'))
      self.assertEqual(
          [('original.txt', 'stuff'),
           ('an_attachment.txt',
            mail.EncodedPayload(
                b'SSBoYXZlIGRhdGE=', charset='us-ascii', encoding='base64'))],
          admin_email.attachments)

  def testUpdateFromMimeMessage_FromString(self):
    for mail_class in (mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      admin_email = mail_class()
      admin_email.update_from_mime_message(MIME_MESSAGE_WITH_ATTACHMENT)

      self.assertEqual('Donut <nobody@gmail.com>', admin_email.sender)
      self.assertEqual('test attachment', admin_email.subject)
      self.assertEqual(
          mail.EncodedPayload(b'\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.body)
      self.assertEqual(
          mail.EncodedPayload(b'<br>\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.html)
      self.assertTrue(hasattr(admin_email, 'attachments'))
      self.assertEqual(
          [('an_attachment.txt',
            mail.EncodedPayload(
                b'SSBoYXZlIGRhdGE=', charset='us-ascii', encoding='base64'))],
          admin_email.attachments)

  def testUpdateFromMimeMessage_FromFile(self):
    for mail_class in (mail.EmailMessage,
                       mail.AdminEmailMessage,
                       mail.InboundEmailMessage):
      mime_message = six.StringIO(MIME_MESSAGE_WITH_ATTACHMENT)
      admin_email = mail_class()
      admin_email.update_from_mime_message(mime_message)

      self.assertEqual('Donut <nobody@gmail.com>', admin_email.sender)
      self.assertEqual('test attachment', admin_email.subject)
      self.assertEqual(
          mail.EncodedPayload(b'\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.body)
      self.assertEqual(
          mail.EncodedPayload(b'<br>\n', charset='iso-8859-1', encoding='7bit'),
          admin_email.html)
      self.assertTrue(hasattr(admin_email, 'attachments'))
      self.assertEqual(
          [('an_attachment.txt',
            mail.EncodedPayload(
                b'SSBoYXZlIGRhdGE=', charset='us-ascii', encoding='base64'))],
          admin_email.attachments)

  def doTestEmailMessageAddressField(self, field):
    mime_message = email.message.Message()
    mime_message[field] = 'nobody@google.com'

    normal_email = mail.EmailMessage()
    normal_email.update_from_mime_message(mime_message)

    self.assertEqual('nobody@google.com', getattr(normal_email, field))

    mime_message[field] = 'nobody2@google.com'

    normal_email.update_from_mime_message(mime_message)
    self.assertEqual(['nobody@google.com', 'nobody2@google.com'],
                     getattr(normal_email, field))

  def testUpdateFromMimeMessage_EmailMessageTo(self):
    self.doTestEmailMessageAddressField('to')

  def testUpdateFromMimeMessage_EmailMessageCc(self):
    self.doTestEmailMessageAddressField('cc')

  def testUpdateFromMimeMessage_EmailMessageBcc(self):
    self.doTestEmailMessageAddressField('bcc')

  def testBodies_NoBodies(self):
    email_message = mail.EmailMessage()

    self.assertEqual([], list(email_message.bodies()))

  def testBodies_TextBody(self):
    email_message = mail.EmailMessage(body='my body')

    self.assertEqual([('text/plain', 'my body')], list(email_message.bodies()))

  def testBodies_HtmlBody(self):
    email_message = mail.EmailMessage(html='my html body')

    self.assertEqual([('text/html', 'my html body')],
                     list(email_message.bodies()))

  def testBodies_BothBodies(self):
    email_message = mail.EmailMessage(body='my body', html='my html body')

    self.assertEqual([
        ('text/html', 'my html body'),
        ('text/plain', 'my body'),
    ], list(email_message.bodies()))

  def testBodiesFilter_NoMatch(self):
    """Test when filtering with unused content type."""
    email_message = mail.EmailMessage(body='my body', html='my html body')

    self.assertEqual([], list(email_message.bodies('image/png')))

  def testBodiesFilter_FullMatch(self):
    """Matching against a whole content-type."""
    email_message = mail.EmailMessage(body='my body', html='my html body')

    self.assertEqual([
        ('text/html', 'my html body'),
    ], list(email_message.bodies('text/html')))

  def testBodiesFilter_PartialMatch(self):
    """Matching against a partial content-type."""
    email_message = mail.EmailMessage(body='my body', html='my html body')

    self.assertEqual([
        ('text/html', 'my html body'),
        ('text/plain', 'my body'),
    ], list(email_message.bodies('text')))


    self.assertEqual([], list(email_message.bodies('tex')))


class SendMailTest(absltest.TestCase):
  """Unit test for send_mail."""

  def DoTestWithStatus(self, expected_status):
    """Perform general send_mail with expected status.

    Args:
      expected_status: Expected status, if not OK, will raise exception. Doing
        is used to ensure that the send_mail function passes on the error it
        receives from the api proxy.
    """
    positional = [
      'from@nowhere.com',
      ['to@nowhere.com'],
      'subject',
      'body',
    ]
    parameters = {
      'cc':        ['cc@nowhere.com'],
      'bcc':       ['bcc@nowhere.com'],
      'reply_to':  'reply@nowhere.com',
    }

    def FakeMakeSyncCall(service, method, request, response):
      """Does fake synchronous API call.

      Arguments match what is expected of apiproxy_stub_map.MakeSyhnCall.
      Checks that service and method name are as expected.

      Args: service
      """
      self.assertEqual('mail', service)
      self.assertEqual('Send', method)


      expected_message = mail.EmailMessage(**parameters)
      (expected_message.sender,
       expected_message.to,
       expected_message.subject,
       expected_message.body) = positional

      self.assertEqual(expected_message.ToProto(), request)

      if expected_status != mail_service_pb2.MailServiceError.OK:
        raise apiproxy_errors.ApplicationError(expected_status,
                                               'expected error')


    mail.send_mail(make_sync_call=FakeMakeSyncCall, *positional, **parameters)

  def testSendMailSuccess(self):
    """Test the case where sendmail results are ok."""
    self.DoTestWithStatus(mail_service_pb2.MailServiceError.OK)

  def testSendMailFailure(self):
    """Test the case where an error occurs.

    Used to ensure that exception from MakeSyncCall is propagated.
    """
    self.assertRaises(mail.BadRequestError, self.DoTestWithStatus,
                      mail_service_pb2.MailServiceError.BAD_REQUEST)

    self.assertRaises(mail.InvalidSenderError, self.DoTestWithStatus,
                      mail_service_pb2.MailServiceError.UNAUTHORIZED_SENDER)

    self.assertRaises(mail.InvalidAttachmentTypeError, self.DoTestWithStatus,
                      mail_service_pb2.MailServiceError.INVALID_ATTACHMENT_TYPE)

  def testSendMailFailureTransmitsErrorMessage(self):
    """Tests that error messages from the server are transmitted."""
    with self.assertRaisesRegex(mail.InvalidSenderError, 'expected error'):
      self.DoTestWithStatus(
          mail_service_pb2.MailServiceError.UNAUTHORIZED_SENDER)


class SendMailToAdminsTest(absltest.TestCase):
  """Unit test for send_mail_to_admins."""

  def DoTestWithStatus(self, expected_status):
    """Perform general send_mail_to_admins with expected status.

    Args:
      expected_status: Expected status, if not OK, will raise exception.
        Doing is used to ensure that the send_mail function passes on the
        error it receives from the api proxy.
    """
    positional = [
      'from@nowhere.com',
      'subject',
      'body',
    ]
    parameters = {
      'reply_to':  'reply@nowhere.com',
    }

    def FakeMakeSyncCall(service, method, request, response):
      """Does fake synchronous API call.

      Arguments match what is expected of apiproxy_stub_map.MakeSyhnCall.
      Checks that service and method name are as expected.

      Args:
        service
      """
      self.assertEqual('mail', service)
      self.assertEqual('SendToAdmins', method)


      expected_message = mail.AdminEmailMessage(**parameters)
      (expected_message.sender,
       expected_message.subject,
       expected_message.body) = positional

      self.assertEqual(expected_message.ToProto(), request)

      if expected_status != mail_service_pb2.MailServiceError.OK:
        raise apiproxy_errors.ApplicationError(expected_status)


    mail.send_mail_to_admins(make_sync_call=FakeMakeSyncCall,
                             *positional,
                             **parameters)

  def testSendMailSuccess(self):
    """Test the case where sendmail results are ok."""
    self.DoTestWithStatus(mail_service_pb2.MailServiceError.OK)

  def testSendMailFailure(self):
    """Test the case where an error occurs.

    Used to ensure that exception from MakeSyncCall is propagated.
    """
    self.assertRaises(mail.BadRequestError, self.DoTestWithStatus,
                      mail_service_pb2.MailServiceError.BAD_REQUEST)

    self.assertRaises(mail.InvalidSenderError, self.DoTestWithStatus,
                      mail_service_pb2.MailServiceError.UNAUTHORIZED_SENDER)

    self.assertRaises(mail.InvalidAttachmentTypeError, self.DoTestWithStatus,
                      mail_service_pb2.MailServiceError.INVALID_ATTACHMENT_TYPE)


RUSSIA_UTF8 = b'\xd0\xa0\xd0\xbe\xd1\x81\xd1\x81\xd0\xb8\xd1\x8f'
RUSSIA_UNICODE = u'\u0420\u043e\u0441\u0441\u0438\u044f'
BINARY_INFO = zlib.compress(b'This is a binary object')


class EncodedPayloadTest(absltest.TestCase):

  def testDecode_NotEncoded(self):
    self.assertEqual(b'plain old data',
                     mail.EncodedPayload(b'plain old data').decode())

  def testDecode_CharsetOnly(self):
    self.assertEqual(RUSSIA_UNICODE,
                     mail.EncodedPayload(RUSSIA_UTF8, 'utf-8').decode())

  def testDecode_EncodingOnly(self):
    self.assertEqual(
        b'Some text.',
        mail.EncodedPayload(zlib.compress(b'Some text.'),
                            encoding='zip').decode())

  def testDecode_Full(self):
    self.assertEqual(
        RUSSIA_UNICODE,
        mail.EncodedPayload(zlib.compress(RUSSIA_UTF8), 'utf-8',
                            'zip').decode())

  def testDecode_BinaryFormat(self):
    self.assertEqual(
        BINARY_INFO,
        mail.EncodedPayload(base64.encodebytes(BINARY_INFO),
                            'base64').decode())

  def testDecode_7bit(self):
    self.assertEqual(b'Still 7 bit',
                     mail.EncodedPayload(b'Still 7 bit', '7bit').decode())

  def testDecode_DoNotKnowHow(self):
    self.assertRaises(
        mail.UnknownCharsetError,
        mail.EncodedPayload(b'something strange', 'wackycoding').decode)
    self.assertRaises(
        mail.UnknownEncodingError,
        mail.EncodedPayload(b'something strange',
                            encoding='wackycoding').decode)

  def testEquality(self):
    self.assertEqual(
        mail.EncodedPayload(b'payload', '7bit', 'zip'),
        mail.EncodedPayload(b'payload', '7bit', 'zip'))
    self.assertEqual(
        mail.EncodedPayload(b'payload', '7bit'),
        mail.EncodedPayload(b'payload', '7bit'))
    self.assertEqual(
        mail.EncodedPayload(b'payload'), mail.EncodedPayload(b'payload'))

    self.assertNotEqual(
        mail.EncodedPayload(b'payload1', '7bit', 'zip'),
        mail.EncodedPayload(b'payload2', '7bit', 'zip'))
    self.assertNotEqual(
        mail.EncodedPayload(b'payload', '7bit', 'zip'),
        mail.EncodedPayload(b'payload', 'utf-8', 'zip'))
    self.assertNotEqual(
        mail.EncodedPayload(b'payload', '7bit', 'zip'),
        mail.EncodedPayload(b'payload', '7bit', 'base64'))

  def testHash(self):
    self.assertEqual(
        hash(mail.EncodedPayload(b'payload', '7bit', 'zip')),
        hash(mail.EncodedPayload(b'payload', '7bit', 'zip')))
    self.assertEqual(
        hash(mail.EncodedPayload(b'payload', '7bit')),
        hash(mail.EncodedPayload(b'payload', '7bit')))
    self.assertEqual(
        hash(mail.EncodedPayload(b'payload')),
        hash(mail.EncodedPayload(b'payload')))

    self.assertNotEqual(
        hash(mail.EncodedPayload(b'payload1', '7bit', 'zip')),
        hash(mail.EncodedPayload(b'payload2', '7bit', 'zip')))
    self.assertNotEqual(
        hash(mail.EncodedPayload(b'payload', '7bit', 'zip')),
        hash(mail.EncodedPayload(b'payload', 'utf-8', 'zip')))
    self.assertNotEqual(
        hash(mail.EncodedPayload(b'payload', '7bit', 'zip')),
        hash(mail.EncodedPayload(b'payload', '7bit', 'base64')))

  def testCopyTo_NotEncoded(self):
    message = email.message.Message()
    payload = mail.EncodedPayload(b'payload')
    payload.copy_to(message)
    self.assertEqual(b'payload', message.get_payload(decode=True))
    self.assertEqual(None, message.get_param('charset'))
    self.assertEqual(None, message['content-transfer-encoding'])

  def testCopyTo_CharsetOnly(self):
    message = email.message.Message()
    payload = mail.EncodedPayload(RUSSIA_UTF8, 'utf-8')
    payload.copy_to(message)
    self.assertEqual(
        base64.encodebytes(RUSSIA_UTF8),
        message.get_payload().encode('utf-8'))
    self.assertEqual('utf-8', message.get_param('charset'))
    self.assertEqual('base64', message['content-transfer-encoding'])

  def testCopyTo_CharsetOnlyUseDefaultEncoding(self):
    message = email.message.Message()
    message['content-type'] = 'text/plain; charset=utf-8'
    payload = mail.EncodedPayload(RUSSIA_UTF8, encoding='utf-8')
    payload.copy_to(message)
    self.assertEqual(RUSSIA_UTF8, message.get_payload(decode=True))
    self.assertEqual('utf-8', message.get_param('charset'))
    self.assertEqual('utf-8', message['content-transfer-encoding'])

  def testCopyTo_EncodingOnly(self):
    payload_zip = zlib.compress(b'payload')
    message = email.message.Message()
    payload = mail.EncodedPayload(payload_zip, encoding='zip')
    payload.copy_to(message)
    self.assertEqual(payload_zip, message.get_payload(decode=True))
    self.assertEqual(None, message.get_param('charset'))
    self.assertEqual('zip', message['content-transfer-encoding'])

  def testCopyTo_Full(self):
    message = email.message.Message()
    payload = mail.EncodedPayload(zlib.compress(RUSSIA_UTF8), 'utf-8', 'zip')
    payload.copy_to(message)
    self.assertEqual(
        zlib.compress(RUSSIA_UTF8), message.get_payload(decode=True))
    self.assertEqual('utf-8', message.get_param('charset'))
    self.assertEqual('zip', message['content-transfer-encoding'])

  def testToMimeMessage(self):
    payload = mail.EncodedPayload(zlib.compress(RUSSIA_UTF8), 'utf-8', 'zip')
    message = payload.to_mime_message()
    self.assertEqual(
        zlib.compress(RUSSIA_UTF8), message.get_payload(decode=True))
    self.assertEqual('utf-8', message.get_param('charset'))
    self.assertEqual('zip', message['content-transfer-encoding'])

  def testStr(self):
    payload = mail.EncodedPayload(zlib.compress(RUSSIA_UTF8), 'utf-8', 'zip')
    message = payload.to_mime_message()
    self.assertEqual(str(message), str(payload))


class InboundEmailMessageTest(absltest.TestCase):
  """Test inbound email sub-class."""

  def testUpdate_DateField(self):
    """Test that date field is properly updated."""
    mime_message = email.message.Message()
    mime_message['Date'] = 'Whatever the date is'

    email_message = mail.InboundEmailMessage()
    email_message.update_from_mime_message(mime_message)

    self.assertEqual('Whatever the date is', email_message.date)

  def testUpdate_MessageId(self):
    """Test that message-id field is properly updated."""
    mime_message = email.message.Message()
    mime_message['Message-id'] = 'Some id'

    email_message = mail.InboundEmailMessage()
    email_message.update_from_mime_message(mime_message)

    self.assertEqual('Some id', email_message.message_id)

  def testUpdate_ExtraText(self):
    """Test that extra text is stored in alternate_bodies."""
    body1 = MIMEText('body1')
    body2 = MIMEText('body2')

    message = MIMEMultipart(_subparts=[body1, body2])

    email_message = mail.InboundEmailMessage(message)

    self.assertEqual('body1', email_message.body.decode())
    self.assertFalse(hasattr(email_message, 'html'))

    ((content_type, payload),) = email_message.alternate_bodies
    self.assertEqual('text/plain', content_type)
    self.assertEqual('body2', payload.decode())

  def testUpdate_ExtraHtml(self):
    """Test that extra html is stored in alternate_bodies."""
    body1 = MIMEText('body1', _subtype='html')
    body2 = MIMEText('body2', _subtype='html')

    message = MIMEMultipart(_subparts=[body1, body2])

    email_message = mail.InboundEmailMessage(message)

    self.assertFalse(hasattr(email_message, 'text'))
    self.assertEqual('body1', email_message.html.decode())

    ((content_type, payload),) = email_message.alternate_bodies
    self.assertEqual('text/html', content_type)
    self.assertEqual('body2', payload.decode())

  def testUpdate_XmlText(self):
    """Test that other text types are always stored in alternate_bodies."""
    body1 = MIMEText('body1', _subtype='xml')

    message = MIMEMultipart(_subparts=[body1])

    email_message = mail.InboundEmailMessage(message)

    self.assertFalse(hasattr(email_message, 'text'))
    self.assertFalse(hasattr(email_message, 'html'))

    ((content_type, payload),) = email_message.alternate_bodies
    self.assertEqual('text/xml', content_type)
    self.assertEqual('body1', payload.decode())

  def testUpdate_BlankBcc(self):
    email_message = mail.InboundEmailMessage(MIME_MESSAGE_BLANK_BCC)

    self.assertEqual('Donut <nobody@gmail.com>', email_message.sender)
    self.assertEqual('Issue 4797: Lotus Notes is Strange',
                     email_message.subject)
    self.assertEqual(
        b'BCC fields with blanks were treated as invalid and '
        b'never reached user code.\n', email_message.body.payload)
    self.assertFalse(hasattr(email_message, 'html'))
    self.assertFalse(hasattr(email_message, 'bcc'))
    self.assertFalse(hasattr(email_message, 'attachments'))
    self.assertTrue(hasattr(email_message, 'to'))

  def testUpdate_MessageWithRfc2047EncodedHeaders(self):
    email_message = mail.InboundEmailMessage(
        MIME_MESSAGE_RFC_2047_ENCODED_PARTS)

    self.assertEqual(u'If you can read this you understand the example.',
                     email_message.subject)

    if six.PY3:
      self.assertEqual(u'Keith Moore  <moore@cs.utk.edu>', email_message.sender)
      self.assertEqual(
          u'Keld J\xf8rn Simonsen  <keld@dkuug.dk>, ' +
          u'Xxx Yyyzzz  <xxx@yyyzzz.appspotmail.com>', email_message.to)
      self.assertEqual(u'Andr\xe9  Pirard <PIRARD@vm1.ulg.ac.be>, xxx@xxx.xx',
                       email_message.cc)
    if six.PY2:
      self.assertEqual(u'Keith Moore <moore@cs.utk.edu>', email_message.sender)
      self.assertEqual(
          u'Keld J\xf8rn Simonsen <keld@dkuug.dk>, ' +
          u'Xxx Yyyzzz <xxx@yyyzzz.appspotmail.com>', email_message.to)
      self.assertEqual(u'Andr\xe9 Pirard <PIRARD@vm1.ulg.ac.be>, xxx@xxx.xx',
                       email_message.cc)

  def testUpdate_NoRecipients(self):
    mime_message_no_recpients = """\
MIME-Version: 1.0
Date: Mon, 17 Oct 2011 15:41:14 -0700
From: Donut <nobody@gmail.com>
Content-Type: text/plain

Very simple message.
"""
    email_message = mail.InboundEmailMessage(mime_message_no_recpients)

    self.assertEqual('Donut <nobody@gmail.com>', email_message.sender)
    self.assertEqual(b'Very simple message.\n', email_message.body.payload)
    self.assertFalse(hasattr(email_message, 'to'))
    self.assertFalse(hasattr(email_message, 'cc'))
    self.assertFalse(hasattr(email_message, 'bcc'))
    self.assertFalse(hasattr(email_message, 'subject'))
    self.assertFalse(hasattr(email_message, 'html'))
    self.assertFalse(hasattr(email_message, 'attachments'))

  def testBodies_BodyPlus(self):
    """Check iteration over bodies with extra body."""
    email_message = mail.InboundEmailMessage(
        body='my body',
        alternate_bodies=[('text/plain', 'alternate1')])

    self.assertEqual([('text/plain', 'my body'), ('text/plain', 'alternate1')],
                     list(email_message.bodies()))

  def testBodies_HtmlPlus(self):
    """Check iteration over bodies with extra html."""
    email_message = mail.InboundEmailMessage(
        html='my html body',
        alternate_bodies=[('text/html', 'alternate1')])

    self.assertEqual([('text/html', 'my html body'),
                      ('text/html', 'alternate1')],
                     list(email_message.bodies()))

  def testBodies_BothPlus(self):
    """Check iteration over bodies with both set and extra."""
    email_message = mail.InboundEmailMessage(
        body='my body',
        html='my html body',
        alternate_bodies=[('text/plain', 'alternate1')])

    self.assertEqual([('text/html', 'my html body'), ('text/plain', 'my body'),
                      ('text/plain', 'alternate1')],
                     list(email_message.bodies()))

  def testBodiesFilter_NoMatch(self):
    """Check when filtering on unused content-type."""
    email_message = mail.InboundEmailMessage(
        body='my body',
        html='my html body',
        alternate_bodies=[('text/plain', 'alternate1')])

    self.assertEqual([], list(email_message.bodies('text/enriched')))

  def testBodiesFilter_FullMatch(self):
    """Check when filtering full content-type."""
    email_message = mail.InboundEmailMessage(
        body='my body',
        html='my html body',
        alternate_bodies=[('text/plain', 'alternate1')])

    self.assertEqual([('text/plain', 'my body'), ('text/plain', 'alternate1')],
                     list(email_message.bodies('text/plain')))

  def testBodiesFilter_PartialMatch(self):
    """Check when filtering full content-type."""
    email_message = mail.InboundEmailMessage(
        body='my body',
        html='my html body',
        alternate_bodies=[('application/pdf', 'alternate1')])

    self.assertEqual([
        ('application/pdf', 'alternate1'),
    ], list(email_message.bodies('application')))


    self.assertEqual([], list(email_message.bodies('applicatio')))

  def testToMimeMessage_NoExtraFields(self):
    """Test converting inbound email to MIME message."""
    message = mail.InboundEmailMessage(sender='nobody@nowhere.com',
                                       to='another@nowhere.com',
                                       subject='a subject',
                                       body='a body')

    mime_message = message.to_mime_message()
    self.assertEqual('multipart/mixed', mime_message['content-type'])
    self.assertEqual('another@nowhere.com', mime_message['to'])
    self.assertEqual('nobody@nowhere.com', mime_message['from'])
    self.assertEqual('a subject', mime_message['subject'])

    (body,) = mime_message.get_payload()
    self.assertEqual('text/plain; charset="us-ascii"', body['content-type'])
    self.assertEqual('a body', body.get_payload())

  def testToMimeMessage_HeaderProperties(self):
    """Test converting inbound email to MIME message."""
    message = mail.InboundEmailMessage(sender='nobody@nowhere.com',
                                       to='another@nowhere.com',
                                       subject='a subject',
                                       body='a body',
                                       date='a date',
                                       message_id='the-id')

    mime_message = message.to_mime_message()
    self.assertEqual('multipart/mixed', mime_message['content-type'])
    self.assertEqual('another@nowhere.com', mime_message['to'])
    self.assertEqual('nobody@nowhere.com', mime_message['from'])
    self.assertEqual('a subject', mime_message['subject'])
    self.assertEqual('a date', mime_message['date'])
    self.assertEqual('the-id', mime_message['message-id'])

    (body,) = mime_message.get_payload()
    self.assertEqual('text/plain; charset="us-ascii"', body['content-type'])
    self.assertEqual('a body', body.get_payload())


class AttachmentTest(absltest.TestCase):

  def testEq(self):
    """Test Attachment.__eq__."""
    self.assertEqual(mail.Attachment('foo.jpg', 'data'), ('foo.jpg', 'data'))
    self.assertEqual(mail.Attachment('foo.jpg', 'data'),
                     mail.Attachment('foo.jpg', 'data'))
    self.assertEqual(mail.Attachment('foo.jpg', 'data', content_id='<foo>'),
                     mail.Attachment('foo.jpg', 'data', content_id='<foo>'))

  def testNe(self):
    """Test Attachment.__ne__."""
    self.assertNotEqual(mail.Attachment('foo.jpg', 'data', content_id='<foo>'),
                        ('foo.jpg', 'data'))
    self.assertNotEqual(mail.Attachment('foo.jpg', 'data'), 1)

  def testUnpack(self):
    """Check that Attachment objects unpack as two-tuples."""
    filename, payload = mail.Attachment('foo.jpg', 'data')
    self.assertEqual(filename, 'foo.jpg')
    self.assertEqual(payload, 'data')



    filename, payload = mail.Attachment('foo.jpg', 'data', content_id='<foo>')
    self.assertEqual(filename, 'foo.jpg')
    self.assertEqual(payload, 'data')

  def testHash(self):
    """Test that Attachment objects hash properly."""
    self.assertEqual(hash(mail.Attachment('foo.jpg', 'data')),
                     hash(('foo.jpg', 'data')))
    self.assertEqual(hash(mail.Attachment('foo.jpg', 'data')),
                     hash(mail.Attachment('foo.jpg', 'data')))
    self.assertEqual(hash(mail.Attachment('foo.jpg',
                                          'data',
                                          content_id='<foo>')),
                     hash(mail.Attachment('foo.jpg',
                                          'data',
                                          content_id='<foo>')))

  def testIndex(self):
    attachment = mail.Attachment('foo.jpg', 'data')
    self.assertEqual(attachment[0], 'foo.jpg')
    self.assertEqual(attachment[1], 'data')

  def testContains(self):
    attachment = mail.Attachment('foo.jpg', 'data')
    self.assertIn('foo.jpg', attachment)
    self.assertIn('data', attachment)

  def testLen(self):
    self.assertEqual(len(mail.Attachment('foo.jpg', 'data')), 2)

if __name__ == '__main__':
  absltest.main()
