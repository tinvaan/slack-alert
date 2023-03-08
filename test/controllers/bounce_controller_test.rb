# frozen_string_literal: true

require 'test_helper'

class BounceControllerTest < ActionDispatch::IntegrationTest
  test 'should raise bad request error' do
    post bounce_notify_url, headers: { "Content-Type": 'application/json' }, params: {}
    assert_response 400

    post bounce_notify_url, headers: { "Content-Type": 'application/json' }, params: {
      "foo": 'bar',
      "bar": 'baz',
      "error": nil,
      "success": nil
    }
    assert_response 400
  end

  test 'should enqueue notify job' do
    payload = {
      "RecordType": 'Bounce',
      "Type": 'SpamNotification',
      "TypeCode": 512,
      "Name": 'Spam notification',
      "Tag": '',
      "MessageStream": 'outbound',
      "Description": 'The message was delivered, but was either blocked by the user, or classified as spam, bulk mail, or had rejected content.',
      "Email": 'zaphod@example.com',
      "From": 'notifications@honeybadger.io',
      "BouncedAt": '2023-02-27T21:41:30Z'
    }
    post bounce_notify_url, headers: { "Content-Type": 'application/json' }, params: JSON.dump(payload)
    assert_response :success
  end

  test 'should not enqueue notify job' do
    payload = {
      "RecordType": 'Bounce',
      "MessageStream": 'outbound',
      "Type": 'HardBounce',
      "TypeCode": 1,
      "Name": 'Hard bounce',
      "Tag": 'Test',
      "Description": 'The server was unable to deliver your message (ex: unknown user, mailbox not found).',
      "Email": 'arthur@example.com',
      "From": 'notifications@honeybadger.io',
      "BouncedAt": '2019-11-05T16:33:54.9070259Z'
    }
    post bounce_notify_url, headers: { "Content-Type": 'application/json' }, params: JSON.dump(payload)
    assert_response 200
  end
end
