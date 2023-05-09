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


"""Unit-test for google.appengine.api.mail_stub module"""



from email import charset
import logging
import os
import re
import shutil
import smtplib
import subprocess
import sys
import tempfile
import google
import mox
import six
from six.moves import map
from google.appengine.api import api_base_pb2
from google.appengine.api import mail
from google.appengine.api import mail_service_pb2
from google.appengine.api import mail_stub
from google.appengine.api import mail_stub_service_pb2
from google.appengine.runtime import apiproxy_errors
from absl.testing import absltest


class MailServiceStubTest(absltest.TestCase):
  """Tests mail service stub"""

  def setUp(self):
    """Set up test harness."""
    if six.PY2:

      reload(sys)
      sys.setdefaultencoding('ascii')

    self.mox = mox.Mox()
    self.popen = self.mox.CreateMockAnything(subprocess.Popen)
    self.smtp = self.mox.CreateMockAnything(smtplib.SMTP)

  def CreateRequest(self, email_type=mail.EmailMessage, **parameters):
    """Create an instance of mail.EmailMessage.

    Args:
      email_type: The class of email message to that will be initialized with
        the parameters kwargs.
      **parameters: Kwargs for initializing the email_type.

    Returns:
      An instance of email_type.
    """
    return email_type(**parameters)

  def DoNothing(self, *params):
    pass

  def CompareMessages(self, message1, message2):
    """Compare two mail._EmailMessageBase instances.

    Args:
      message1: First message.
      message2: Second message.
    """
    for property_name in mail._EmailMessageBase.PROPERTIES:
      if hasattr(message1, property_name) or hasattr(message2, property_name):
        prop1 = getattr(message1, property_name)
        if isinstance(prop1, mail.EncodedPayload):
          prop1 = prop1.decode()
        prop2 = getattr(message2, property_name)
        if isinstance(prop2, mail.EncodedPayload):
          prop2 = prop2.decode()
        self.assertEqual(prop1, prop2)

  def testSendBasic(self):
    """Test basic logging with minimal fields, both text bodies."""
    mail_service = mail_stub.MailServiceStub()
    results = []
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    mail_service._Send(message.ToProto(),
                       None,
                       results.append,
                       self.smtp,
                       self.popen)
    self.assertListEqual(
      ['MailService.Send\n'
       '  From: from@nowhere.com\n'
       '  To: to@nowhere.com\n'
       '  Subject: a subject\n'
       '  Body:\n'
       '    Content-type: text/plain\n'
       '    Data length: %d\n' % len('a body') +
       '  Body:\n'
       '    Content-type: text/html\n'
       '    Data length: %d' % len('<html>')
      ],
      results)

  def testSendAmpEmail(self):
    """Test basic logging with minimal fields, with text, HTML, and AMP HTML."""
    mail_service = mail_stub.MailServiceStub()
    results = []
    message = self.CreateRequest(
        sender='from@nowhere.com',
        to=['to@nowhere.com'],
        subject='a subject',
        body='a body',
        html='<html>',
        amp_html='<html ⚡4email></html>')
    mail_service._Send(message.ToProto(), None, results.append, self.smtp,
                       self.popen)
    self.assertListEqual([
        'MailService.Send\n'
        '  From: from@nowhere.com\n'
        '  To: to@nowhere.com\n'
        '  Subject: a subject\n'
        '  Body:\n'
        '    Content-type: text/plain\n'
        '    Data length: %d\n' % len(u'a body') + '  Body:\n'
        '    Content-type: text/x-amp-html\n'
        '    Data length: %d\n' % len(u'<html ⚡4email></html>') + '  Body:\n'
        '    Content-type: text/html\n'
        '    Data length: %d' % len(u'<html>')
    ], results)

  def testSendBlacklistedAttachmentFails(self):
    """Test that a blacklisted extension type fails."""
    mail_service = mail_stub.MailServiceStub()
    message = mail_service_pb2.MailMessage()
    attachment = message.Attachment.add()
    attachment.FileName = 'uhoh.exe'
    attachment.Data = b'uhoh'

    self.assertRaises(apiproxy_errors.ApplicationError,
                      mail_service._Send,
                      message,
                      None,
                      logging.info,
                      self.smtp,
                      self.popen)

  def testSendHiddenFileAttachmentFails(self):
    """Test that a filename starting with a period fails."""
    mail_service = mail_stub.MailServiceStub()
    message = mail_service_pb2.MailMessage()
    attachment = message.Attachment.add()
    attachment.FileName = '.hidden'
    attachment.Data = u'uhoh'.encode('utf-8')

    self.assertRaises(apiproxy_errors.ApplicationError,
                      mail_service._Send,
                      message,
                      None,
                      logging.info,
                      self.smtp,
                      self.popen)

  def testSendExtensionlessAttachmentFails(self):
    """Test that a file without an extension fails."""
    mail_service = mail_stub.MailServiceStub()
    message = mail_service_pb2.MailMessage()
    attachment = message.Attachment.add()
    attachment.FileName = 'uhoh'
    attachment.Data = u'uhoh'.encode('utf-8')

    self.assertRaises(apiproxy_errors.ApplicationError,
                      mail_service._Send,
                      message,
                      None,
                      logging.info,
                      self.smtp,
                      self.popen)

  def testSendBasicWithLoggedBody(self):
    """Test basic logging with minimal fields, and a logged bodies."""
    mail_service = mail_stub.MailServiceStub(show_mail_body=True)
    results = []
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    mail_service._Send(message.ToProto(),
                       None,
                       results.append,
                       self.smtp,
                       self.popen)
    self.assertListEqual(
      ['MailService.Send\n'
       '  From: from@nowhere.com\n'
       '  To: to@nowhere.com\n'
       '  Subject: a subject\n'
       '  Body:\n'
       '    Content-type: text/plain\n'
       '    Data length: %d\n' % len('a body') +
       '-----\na body\n-----\n'
       '  Body:\n'
       '    Content-type: text/html\n'
       '    Data length: %d\n' % len('<html>') +
       '-----\n<html>\n-----'
      ],
      results)

  def testSendToAdmins(self):
    """Test basic logging with minimal fields, only text body for admins."""
    mail_service = mail_stub.MailServiceStub()
    results = []
    message = self.CreateRequest(sender='from@nowhere.com',
                                 subject='a subject',
                                 body='a body',
                                 email_type=mail.AdminEmailMessage)
    mail_service._SendToAdmins(message.ToProto(),
                               None,
                               results.append)
    self.assertListEqual(
      ['MailService.SendToAdmins\n'
       '  From: from@nowhere.com\n'
       '  Subject: a subject\n'
       '  Body:\n'
       '    Content-type: text/plain\n'
       '    Data length: %d' % len('a body')
      ],
      results)

  def testSendOnlyHtml(self):
    """Test basic logging with minimal fields, only html body."""
    mail_service = mail_stub.MailServiceStub()
    results = []
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 html='<html>')
    mail_service._Send(message.ToProto(),
                       None,
                       results.append,
                       self.smtp,
                       self.popen)
    self.assertListEqual(
      ['MailService.Send\n'
       '  From: from@nowhere.com\n'
       '  To: to@nowhere.com\n'
       '  Subject: a subject\n'
       '  Body:\n'
       '    Content-type: text/html\n'
       '    Data length: %d' % len('<html>')
      ],
      results)

  def testSendFull(self):
    """Test logging with multiple values and all fields."""
    mail_service = mail_stub.MailServiceStub('smtp-host',
                                             25,
                                             'smtp-user',
                                             'smtp-password',
                                             True,
                                             allow_tls=True)
    results = []
    message = self.CreateRequest(
        sender='from@nowhere.com',
        to=['to1@nowhere.com', 'to2@nowhere.com'],
        subject='a subject',
        body='a body',
        html='<html>',
        amp_html='<html ⚡4email></html>',
        cc=['cc1@nowhere.com', 'cc2@nowhere.com'],
        bcc=['bcc1@nowhere.com', 'bcc2@nowhere.com'],
        reply_to='replyto@nowhere.com',
        attachments=[('html.html', 'html1'), ('txt.txt', 'txt1'),
                     ('sub.dir/jpeg.jpg', 'jpg1')])
    smtp_object = self.mox.CreateMock(smtplib.SMTP)
    self.smtp().AndReturn(smtp_object)
    smtp_object.connect('smtp-host', 25)
    smtp_object.ehlo_or_helo_if_needed()
    smtp_object.has_extn('STARTTLS').AndReturn(True)
    smtp_object.starttls()
    smtp_object.ehlo()
    smtp_object.login('smtp-user', 'smtp-password')
    smtp_object.sendmail(
        mox.IgnoreArg(), mox.IgnoreArg(),
        mox.StrContains(
            'Content-Type: image/jpeg\n'
            'MIME-Version: 1.0\n'
            'Content-Disposition: attachment; filename="sub.dir/jpeg.jpg"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'anBnMQ==\n'))
    smtp_object.quit()
    self.mox.ReplayAll()
    mail_service._enable_sendmail = False
    mail_service._Send(message.ToProto(),
                       None,
                       results.append,
                       self.smtp,
                       self.popen)
    self.assertListEqual([
        'MailService.Send\n'
        '  From: from@nowhere.com\n'
        '  To: to1@nowhere.com\n'
        '  To: to2@nowhere.com\n'
        '  Cc: cc1@nowhere.com\n'
        '  Cc: cc2@nowhere.com\n'
        '  Bcc: bcc1@nowhere.com\n'
        '  Bcc: bcc2@nowhere.com\n'
        '  Reply-to: replyto@nowhere.com\n'
        '  Subject: a subject\n'
        '  Body:\n'
        '    Content-type: text/plain\n'
        '    Data length: %d\n' % len(u'a body') + '  Body:\n'
        '    Content-type: text/x-amp-html\n'
        '    Data length: %d\n' % len(u'<html ⚡4email></html>') + '  Body:\n'
        '    Content-type: text/html\n'
        '    Data length: %d\n' % len(u'<html>') + '  Attachment:\n'
        '    File name: html.html\n'
        '    Data length: %d\n' % len(u'html1') + '  Attachment:\n'
        '    File name: txt.txt\n'
        '    Data length: %d\n' % len(u'txt1') + '  Attachment:\n'
        '    File name: sub.dir/jpeg.jpg\n'
        '    Data length: %d' % len(u'jpg1')
    ], results)
    self.mox.VerifyAll()

  def testSendSendmail(self):
    """Tests sending via sendmail."""
    mail_service = mail_stub.MailServiceStub(enable_sendmail=True)
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 cc=['cc1@nowhere.com',
                                     'cc2@nowhere.com'],
                                 bcc=['blind <bcc@nowhere.com>'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')

    send = self.mox.CreateMockAnything()
    receive = self.mox.CreateMockAnything()
    child = self.mox.CreateMock(subprocess.Popen)
    child.stdin = send
    child.stdout = receive
    self.popen('sendmail \'to@nowhere.com\' \'cc1@nowhere.com\' '
               '\'cc2@nowhere.com\' \'blind <bcc@nowhere.com>\'',
               shell=True,
               stdin=subprocess.PIPE,
               stdout=subprocess.PIPE).AndReturn(child)

    send.write(
        mox.Regex(b'(?s)^(?!From ).*' +
                  re.escape(b'MIME-Version: 1.0\n'
                            b'To: to@nowhere.com\n'
                            b'Cc: cc1@nowhere.com, cc2@nowhere.com\n'
                            b'Bcc: blind <bcc@nowhere.com>\n'
                            b'From: from@nowhere.com\n'
                            b'Reply-To: \n'
                            b'Subject: a subject\n\n')))
    send.close()
    child.poll().AndReturn(None)
    receive.read(100)
    child.poll().AndReturn(None)
    receive.read(100)
    child.poll().AndReturn(0)
    receive.close()
    self.mox.ReplayAll()

    mail_service._Send(message.ToProto(),
                       None,
                       self.DoNothing,
                       self.smtp,
                       self.popen)

    self.mox.VerifyAll()

  def testSendSendmailIO(self):
    """Tests sending via sendmail IO works propertly."""
    mail_service = mail_stub.MailServiceStub(enable_sendmail=True)
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')

    temp_dir = tempfile.mkdtemp()
    try:
      sendmail_script = os.path.join(temp_dir, 'sendmail')
      sendmail_input = os.path.join(temp_dir, 'input')
      sendmail_file = open(sendmail_script, 'w')


      sendmail_file.write('cat > "%s"\n' % sendmail_input)
      sendmail_file.close()


      sendmail_command = '/bin/bash %s' % sendmail_script
      mail_service._Send(message.ToProto(),
                         None,
                         self.DoNothing,
                         self.smtp,
                         sendmail_command=sendmail_command)


      result = open(sendmail_input, 'r').read()
      self.assertNotEqual(
          -1,
          result.find('MIME-Version: 1.0\n'
                      'To: to@nowhere.com\n'
                      'From: from@nowhere.com\n'
                      'Reply-To: \n'
                      'Subject: a subject\n\n'))

      self.assertEqual(-1, result.find('From '))
    finally:
      shutil.rmtree(temp_dir)

  def testSendSMTP(self):
    """Tests that sendmail is not used when SMTP is configured."""
    mail_service = mail_stub.MailServiceStub('smtp-host',
                                             25,
                                             'smtp-user',
                                             'smtp-password',
                                             True,
                                             allow_tls=True)
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 cc=['cc@nowhere.com'],
                                 bcc=['bcc@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')

    smtp_object = self.mox.CreateMock(smtplib.SMTP)
    self.smtp().AndReturn(smtp_object)
    smtp_object.connect('smtp-host', 25)
    smtp_object.ehlo_or_helo_if_needed()
    smtp_object.has_extn('STARTTLS').AndReturn(False)
    smtp_object.login('smtp-user', 'smtp-password')
    smtp_object.sendmail('from@nowhere.com',
                         ['to@nowhere.com',
                          'cc@nowhere.com',
                          'bcc@nowhere.com'],

                         mox.Regex('(?s)^(?!From ).*' +
                                   re.escape('MIME-Version: 1.0\n'
                                             'To: to@nowhere.com\n'
                                             'Cc: cc@nowhere.com\n'
                                             'Bcc: bcc@nowhere.com\n'
                                             'From: from@nowhere.com\n'
                                             'Reply-To: \n'
                                             'Subject: a subject\n\n')))
    smtp_object.quit()
    self.mox.ReplayAll()
    mail_service._Send(message.ToProto(),
                       None,
                       self.DoNothing,
                       self.smtp,
                       self.popen)

    self.mox.VerifyAll()

  def testSendSMTPDisableTls(self):
    """Tests the ability to disable TLS for SMTP.

    Note: testSendFull tests when the server announces TLS and we use it,
    testSendSMTP checks when server does not announce TLS.
    """
    mail_service = mail_stub.MailServiceStub('smtp-host',
                                             25,
                                             'smtp-user',
                                             'smtp-password',
                                             True,
                                             allow_tls=False)
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 cc=['cc@nowhere.com'],
                                 bcc=['bcc@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')

    smtp_object = self.mox.CreateMock(smtplib.SMTP)
    self.smtp().AndReturn(smtp_object)
    smtp_object.connect('smtp-host', 25)
    smtp_object.ehlo_or_helo_if_needed()
    smtp_object.login('smtp-user', 'smtp-password')
    smtp_object.sendmail('from@nowhere.com',
                         ['to@nowhere.com',
                          'cc@nowhere.com',
                          'bcc@nowhere.com'],

                         mox.Regex('(?s)^(?!From ).*' +
                                   re.escape('MIME-Version: 1.0\n'
                                             'To: to@nowhere.com\n'
                                             'Cc: cc@nowhere.com\n'
                                             'Bcc: bcc@nowhere.com\n'
                                             'From: from@nowhere.com\n'
                                             'Reply-To: \n'
                                             'Subject: a subject\n\n')))
    smtp_object.quit()
    self.mox.ReplayAll()
    mail_service._Send(message.ToProto(),
                       None,
                       self.DoNothing,
                       self.smtp,
                       self.popen)

    self.mox.VerifyAll()

  def testSendWithEmailModuleDropped(self):
    """Test usability of _Send() after email was dropped from sys.modules.

    The email package employs its own import magic in email/__init__.py.  This
    makes it break in case the dev_appserver has thrown all modules away (e.g.
    after the user has modified some file).

    For this test we've imported email above at module level, now we drop it
    from sys.modules and make sure _Send is still working.
    """
    assert 'email' in sys.modules
    del sys.modules['email']
    self.testSendSendmail()

  def testCachingMessagesWorks(self):
    """Test that caching messages works as expected.

    Whenever we call _Send() we should be caching the message.
    """
    mail_service = mail_stub.MailServiceStub()

    self.assertFalse(mail_service._cached_messages)

    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    mail_service._Send(message.ToProto(),
                       None,
                       self.DoNothing,
                       self.smtp,
                       self.popen)
    self.assertLen(mail_service._cached_messages, 1)


    mail_service._CacheMessage(message)
    self.assertLen(mail_service._cached_messages, 2)

  def testGetSentMessages(self):
    """Test that get_sent_messages() gives back cached messages."""
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    self.assertFalse(mail_service.get_sent_messages())

    mail_service._CacheMessage(message)
    retrieved_messages = mail_service.get_sent_messages()
    self.assertLen(retrieved_messages, 1)
    self.CompareMessages(message, retrieved_messages[0])

  def testGetSentMessagesFilteredByToFieldList(self):
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com', 'anotherto@nowhere,com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    mail_service._CacheMessage(message)
    filtered_messages = mail_service.get_sent_messages(to='to@nowhere.com')
    self.assertLen(filtered_messages, 1)
    self.CompareMessages(message, filtered_messages[0])

    filtered_messages = mail_service.get_sent_messages(
        to='anotherto@nowhere.com')
    self.assertLen(filtered_messages, 1)
    self.CompareMessages(message, filtered_messages[0])

    missing_messages = mail_service.get_sent_messages(to='missing@nowhere.com')
    self.assertFalse(missing_messages)

    mail_service._CacheMessage(message)
    filtered_messages = mail_service.get_sent_messages(to='to@nowhere.com')
    self.assertLen(filtered_messages, 2)

    filtered_messages = mail_service.get_sent_messages(
        to='anotherto@nowhere.com')
    self.assertLen(filtered_messages, 2)

  def testGetSentMessagesFilteredByToField(self):
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to='to@nowhere.com',
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    mail_service._CacheMessage(message)
    filtered_messages = mail_service.get_sent_messages(to='to@nowhere.com')
    self.assertLen(filtered_messages, 1)
    self.CompareMessages(message, filtered_messages[0])

    missing_messages = mail_service.get_sent_messages(to='missing@nowhere.com')
    self.assertFalse(missing_messages)

    mail_service._CacheMessage(message)
    filtered_messages = mail_service.get_sent_messages(to='to@nowhere.com')
    self.assertLen(filtered_messages, 2)

  def testGetSentMessagesFilteredBySenderField(self):
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@place.com',
                                 to=['to@place.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    mail_service._CacheMessage(message)
    self.assertLen(mail_service.get_sent_messages(), 1)

    filtered_messages = mail_service.get_sent_messages(sender='from@place.com')
    self.assertLen(filtered_messages, 1)
    self.CompareMessages(message, filtered_messages[0])

    missing_messages = mail_service.get_sent_messages(sender='no@place.com')
    self.assertFalse(missing_messages)

    mail_service._CacheMessage(message)
    filtered_messages = mail_service.get_sent_messages(sender='from@place.com')
    self.assertLen(filtered_messages, 2)

  def testGetSentMessagesFitleredBySubjectField(self):
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    mail_service._CacheMessage(message)
    self.assertLen(mail_service.get_sent_messages(), 1)

    filtered_messages = mail_service.get_sent_messages(subject='a subject')
    self.assertLen(filtered_messages, 1)
    self.CompareMessages(message, filtered_messages[0])

    missing_messages = mail_service.get_sent_messages(subject='missing')
    self.assertFalse(missing_messages)

    mail_service._CacheMessage(message)
    filtered_messages = mail_service.get_sent_messages(subject='a subject')
    self.assertLen(filtered_messages, 2)

  def testGetSentMessagesFilteredByBodyField(self):
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    mail_service._CacheMessage(message)
    self.assertLen(mail_service.get_sent_messages(), 1)

    filtered_messages = mail_service.get_sent_messages(body='body')
    self.assertLen(filtered_messages, 1)
    self.CompareMessages(message, filtered_messages[0])

    missing_messages = mail_service.get_sent_messages(body='nothing')
    self.assertFalse(missing_messages)

    mail_service._CacheMessage(message)
    filtered_messages = mail_service.get_sent_messages(body='body')
    self.assertLen(filtered_messages, 2)

  def testGetSentMessagesWithEncodedBodyFilteredByBodyField(self):
    mail_service = mail_stub.MailServiceStub()
    payload = mail.EncodedPayload('body'.encode('utf-8'), encoding='utf-8')
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body=payload,
                                 html='<html>')
    mail_service._CacheMessage(message)
    self.assertLen(mail_service.get_sent_messages(), 1)

    filtered_messages = mail_service.get_sent_messages(body='body')
    self.assertLen(filtered_messages, 1)
    self.CompareMessages(message, filtered_messages[0])

    missing_messages = mail_service.get_sent_messages(body='nothing')
    self.assertFalse(missing_messages)

    mail_service._CacheMessage(message)
    filtered_messages = mail_service.get_sent_messages(body='body')
    self.assertLen(filtered_messages, 2)

  def testGetSentMessagesFilteredByHtmlField(self):
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>Hi!</html>')
    mail_service._CacheMessage(message)
    self.assertLen(mail_service.get_sent_messages(), 1)

    filtered_messages = mail_service.get_sent_messages(html='Hi')
    self.assertLen(filtered_messages, 1)
    self.CompareMessages(message, filtered_messages[0])

    missing_messages = mail_service.get_sent_messages(html='nothing')
    self.assertFalse(missing_messages)

    mail_service._CacheMessage(message)
    filtered_messages = mail_service.get_sent_messages(html='Hi')
    self.assertLen(filtered_messages, 2)

    non_html_message = self.CreateRequest(sender='from@nowhere.com',
                                          to=['to@nowhere.com'],
                                          subject='a subject',
                                          body='a body')
    mail_service._CacheMessage(non_html_message)
    filtered_messages = mail_service.get_sent_messages(html='Hi!')
    self.assertLen(filtered_messages, 2)
    self.CompareMessages(message, filtered_messages[0])
    self.CompareMessages(message, filtered_messages[1])

  def testGetSentMessagesFilteredByHtmlFieldMissing(self):
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body')
    mail_service._CacheMessage(message)
    filtered_messages = mail_service.get_sent_messages(html='anything')
    self.assertFalse(filtered_messages)

  def testGetSentMessagesFilteredByMultipleFields(self):
    mail_service = mail_stub.MailServiceStub()
    message1 = self.CreateRequest(sender='from@nowhere.com',
                                  to=['to@nowhere.com'],
                                  subject='Subject 1',
                                  body='Hi!')
    message2 = self.CreateRequest(sender='from@nowhere.com',
                                  to=['to@nowhere.com'],
                                  subject='Subject 2',
                                  body='Hi again!')

    message3 = self.CreateRequest(sender='from@nowhere.com',
                                  to=['other@nowhere.com'],
                                  subject='Subject 1',
                                  body='Hi again!')

    mail_service._CacheMessage(message1)
    mail_service._CacheMessage(message2)
    mail_service._CacheMessage(message3)
    filtered_messages = mail_service.get_sent_messages()
    self.assertLen(mail_service.get_sent_messages(), 3)
    self.CompareMessages(message1, filtered_messages[0])
    self.CompareMessages(message2, filtered_messages[1])
    self.CompareMessages(message3, filtered_messages[2])

    messages_to_nowhere = mail_service.get_sent_messages(to='to@nowhere.com')
    self.assertLen(messages_to_nowhere, 2)

    messages_subject_1 = mail_service.get_sent_messages(subject='Subject 1')
    self.assertLen(messages_subject_1, 2)

    messages_subject_2 = mail_service.get_sent_messages(subject='Subject 2')
    self.assertLen(messages_subject_2, 1)

    filtered_messages = mail_service.get_sent_messages(to='to@nowhere.com',
                                                       subject='Subject 1')
    self.assertLen(filtered_messages, 1)

    filtered_messages = mail_service.get_sent_messages(to='to@nowhere.com',
                                                       subject='Subject 2')
    self.assertLen(filtered_messages, 1)

    filtered_messages = mail_service.get_sent_messages(to='other@nowhere.com',
                                                       subject='Subject 1')
    self.assertLen(filtered_messages, 1)

  def testGetSentMessagesFilterByRegularExpression(self):
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    mail_service._CacheMessage(message)
    self.assertLen(mail_service.get_sent_messages(), 1)

    filtered_messages = mail_service.get_sent_messages(to='to')
    self.assertLen(filtered_messages, 1)

    filtered_messages = mail_service.get_sent_messages(to=re.compile('to'))
    self.assertLen(filtered_messages, 1)

    filtered_messages = mail_service.get_sent_messages(to=r'to@nowhere\.com')
    self.assertLen(filtered_messages, 1)

    filtered_messages = mail_service.get_sent_messages(to=r'@nowhere\.com$')
    self.assertLen(filtered_messages, 1)

    filtered_messages = mail_service.get_sent_messages(to=r'@somewhere\.com$')
    self.assertFalse(filtered_messages)

    filtered_messages = mail_service.get_sent_messages(sender=r'@nowhere\.com$')
    self.assertLen(filtered_messages, 1)

    filtered_messages = mail_service.get_sent_messages(body=r'body$')
    self.assertLen(filtered_messages, 1)

    filtered_messages = mail_service.get_sent_messages(html=r'html>$')
    self.assertLen(filtered_messages, 1)

  def testGetSentMessagesWithUnicodeInPayload(self):
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body=u'a body using special chars: éèÉ©',
                                 html=u'<html>éèÉ©')
    mail_service._CacheMessage(message)
    retrieved_messages = mail_service.get_sent_messages()
    self.assertLen(retrieved_messages, 1)
    self.CompareMessages(message, retrieved_messages[0])

  def testGetSentMessagesWithUnicodeInHeader(self):
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender=u'Áwêsöme <from@nowhere.com>',
                                 to=[u'Vérÿ Cöôl <to@nowhere.com>'],
                                 cc=[u'Vérÿ Cöôl <to@nowhere.com>'],
                                 bcc=[u'Vérÿ Cöôl <to@nowhere.com>'],
                                 reply_to=u'Áwêsöme <from@nowhere.com>',
                                 subject=u'â sübje©t',
                                 body=u'a body using special chars: éèÉ©',
                                 html=u'<html>éèÉ©')
    mail_service._CacheMessage(message)
    retrieved_messages = mail_service.get_sent_messages()
    self.assertLen(retrieved_messages, 1)
    self.CompareMessages(message, retrieved_messages[0])

  def testGetSentMessagesWithUnicodeInPayloadWith8bitEncoding(self):
    backup_charset = charset.CHARSETS['utf-8']

    charset.add_charset('utf-8', charset.SHORTEST, None, 'utf-8')

    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender=u'Áwêsöme <from@nowhere.com>',
                                 to=[u'Vérÿ Cöôl <to@nowhere.com>'],
                                 subject='a subject',
                                 body=u'a body using special chars: éèÉ©',
                                 html=u'<html>éèÉ©')
    mail_service._CacheMessage(message)
    retrieved_messages = mail_service.get_sent_messages()
    self.assertLen(retrieved_messages, 1)
    self.CompareMessages(message, retrieved_messages[0])


    charset.add_charset(
        'utf-8', backup_charset[0], backup_charset[1], backup_charset[2])

  def testGetSentMessagesWithSendToAdmin(self):
    """Test that get_sent_messages() gives back cached messages."""
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 subject='a subject',
                                 body='a body',
                                 email_type=mail.AdminEmailMessage)
    self.assertFalse(mail_service.get_sent_messages())

    mail_service._CacheMessage(message)
    retrieved_messages = mail_service.get_sent_messages()
    self.assertLen(retrieved_messages, 1)
    self.CompareMessages(message, retrieved_messages[0])

  def testDynamicGetSentMessages(self):
    """Tests that a call to _Dynamic_GetSentMessages returns all messages."""
    mail_service = mail_stub.MailServiceStub()


    message1 = self.CreateRequest(
        sender='from@nowhere.com', to=['to@nowhere.com'],
        subject='a subject', body='a body', html='<html>')
    mail_service._CacheMessage(message1)
    message2 = self.CreateRequest(
        sender='foo@bar.com', to=['bar@foo.com'],
        subject='peekaboo', body='boomeroo', html='<html></html>')
    mail_service._CacheMessage(message2)


    request = api_base_pb2.VoidProto()
    response = mail_stub_service_pb2.GetSentMessagesResponse()
    mail_service._Dynamic_GetSentMessages(request, response)
    retrieved_messages = list(
        map(_EmailMessageFromProto, response.sent_message))


    self.assertLen(retrieved_messages, 2)
    self.CompareMessages(message1, retrieved_messages[0])
    self.CompareMessages(message2, retrieved_messages[1])

  def testDynamicClearSentMessages(self):
    """Tests that _Dynamic_ClearSentMessages clears and returns a count."""
    mail_service = mail_stub.MailServiceStub()
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>')
    self.assertFalse(mail_service.get_sent_messages())
    mail_service._CacheMessage(message)

    request = api_base_pb2.VoidProto()
    response = mail_stub_service_pb2.ClearSentMessagesResponse()
    mail_service._Dynamic_ClearSentMessages(request, response)

    self.assertEqual(1, response.messages_cleared)
    self.assertEmpty(mail_service.get_sent_messages())

  def testNeverDoubleEncodeAttachments(self):
    message = self.CreateRequest(sender='from@nowhere.com',
                                 to=['to@nowhere.com'],
                                 subject='a subject',
                                 body='a body',
                                 html='<html>',
                                 attachments=[('html.html',
                                               'html1'),
                                              ('txt.txt',
                                               'txt1'),
                                              ('sub.dir/jpeg.jpg',
                                               'jpg1')])
    request = message.ToProto()
    mime_message = mail.MailMessageToMIMEMessage(request)


    mail_stub._Base64EncodeAttachments(mime_message)
    item = mime_message.get_payload()[-1]
    self.assertListEqual(
        [('Content-Type', 'image/jpeg'), ('MIME-Version', '1.0'),
         ('Content-Disposition', 'attachment; filename="sub.dir/jpeg.jpg"'),
         ('Content-Transfer-Encoding', 'base64')], list(item.items()))
    self.assertEqual('anBnMQ==', item.get_payload())


    mail_stub._Base64EncodeAttachments(mime_message)
    item = mime_message.get_payload()[-1]
    self.assertListEqual(
        [('Content-Type', 'image/jpeg'), ('MIME-Version', '1.0'),
         ('Content-Disposition', 'attachment; filename="sub.dir/jpeg.jpg"'),
         ('Content-Transfer-Encoding', 'base64')], list(item.items()))
    self.assertEqual('anBnMQ==', item.get_payload())

  def testDecodeHeaderUtf8(self):
    header = mail._decode_and_join_header(
        '=?UTF-8?Q?Unicode=20Apostraphe:=20=28DiRT_=E2=80=9815_test=29?=')
    self.assertEqual(header, u'Unicode Apostraphe: (DiRT \u201815 test)')

  def testDecodeHeaderInvalidUtf8(self):
    header = mail._decode_and_join_header(
        '=?UTF-8?Q?Unicode=20Error:=20=ab=de?=')
    self.assertEqual(header, u'Unicode Error: \ufffd\ufffd')

  def testSendAndGetMessageWithHeaders(self):
    """Retrieving a sent message with headers should return those headers."""
    mail_service = mail_stub.MailServiceStub()

    message = mail_service_pb2.MailMessage()
    message.Sender = 'sender'
    message.To.append('to')
    header = message.Header.add()
    header.name = 'List-Id'
    header.value = 'serverless-cli'

    mail_service._Send(message, None)
    retrieved_message = mail_service.get_sent_messages()[0]

    self.assertIsInstance(retrieved_message, mail.EmailMessage)
    self.assertEqual(retrieved_message.headers['List-Id'], 'serverless-cli')

  def testDynamicGetAndSetLogMailBody(self):
    mail_service = mail_stub.MailServiceStub(show_mail_body=False)


    response = mail_stub_service_pb2.GetLogMailBodyResponse()
    mail_service._Dynamic_GetLogMailBody(api_base_pb2.VoidProto(), response)
    self.assertEqual(response.log_mail_body, False)


    request = mail_stub_service_pb2.SetLogMailBodyRequest()
    request.log_mail_body = True
    mail_service._Dynamic_SetLogMailBody(request, api_base_pb2.VoidProto())
    response = mail_stub_service_pb2.GetLogMailBodyResponse()
    mail_service._Dynamic_GetLogMailBody(api_base_pb2.VoidProto(), response)
    self.assertEqual(response.log_mail_body, True)

  def testDynamicGetAndSetLogMailLevelString(self):
    mail_service = mail_stub.MailServiceStub(enable_sendmail=True)

    request = mail_stub_service_pb2.SetLogMailLevelRequest()
    request.log_mail_level = 'FINE'
    mail_service._Dynamic_SetLogMailLevel(request, api_base_pb2.VoidProto())
    self.assertEqual(logging.DEBUG, mail_service._log_fn.args[0])

    response = mail_stub_service_pb2.GetLogMailLevelResponse()
    mail_service._Dynamic_GetLogMailLevel(api_base_pb2.VoidProto(), response)
    self.assertEqual(response.log_mail_level, 'FINE')

  def testDynamicGetAndSetLogMailLevelInt(self):
    mail_service = mail_stub.MailServiceStub(enable_sendmail=True)

    request = mail_stub_service_pb2.SetLogMailLevelRequest()
    request.log_mail_level = '321'
    mail_service._Dynamic_SetLogMailLevel(request, api_base_pb2.VoidProto())
    self.assertEqual(321, mail_service._log_fn.args[0])

    response = mail_stub_service_pb2.GetLogMailLevelResponse()
    mail_service._Dynamic_GetLogMailLevel(api_base_pb2.VoidProto(), response)
    self.assertEqual(response.log_mail_level, '321')


def _EmailMessageFromProto(mail_message_proto):
  """Returns a mail.EmailMessage from a given mail_service_pb2.MailMessage."""
  kwargs = {
      'to': mail_message_proto.To,
      'sender': mail_message_proto.Sender,
      'subject': mail_message_proto.Subject,
      'body': mail_message_proto.TextBody,
      'html': mail_message_proto.HtmlBody,
  }
  if mail_message_proto.Cc:
    kwargs['cc_list'] = mail_message_proto.Cc
  if mail_message_proto.Bcc:
    kwargs['bcc_list'] = mail_message_proto.Bcc
  if mail_message_proto.Attachment:
    kwargs['attachments'] = mail_message_proto.Attachment
  if mail_message_proto.HasField('ReplyTo'):
    kwargs['reply_to'] = mail_message_proto.ReplyTo

  return mail.EmailMessage(**kwargs)




if __name__ == '__main__':
  absltest.main()
