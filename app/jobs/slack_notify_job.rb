# frozen_string_literal: true

require 'slack-ruby-client'

Slack.configure do |config|
  config.token = ENV['SLACK_BOT_TOKEN']
  raise 'Missing SLACK_BOT_TOKEN!' unless config.token
end

class SlackNotifyJob < ApplicationJob
  queue_as :default

  def perform(*args)
    record = args.pop
    client = Slack::Web::Client.new
    message = [
      {
        'type': 'header',
        'text': {
          'type': 'plain_text',
          'text': record['Name']
        }
      },
      {
        'type': 'section',
        'fields': [
          {
            'type': 'mrkdwn',
            'text': "*Email:* #{record['Email']}"
          }
        ]
      },
      {
        'type': 'section',
        'fields': [
          {
            'type': 'mrkdwn',
            'text': "*When:* #{record['BouncedAt']}"
          }
        ]
      },
      {
        'type': 'section',
        'text': {
          'type': 'mrkdwn',
          'text': "*Description:* #{record['Description']}"
        }
      }
    ]
    client.chat_postMessage(channel: '#spam', blocks: JSON.dump(message))
  end
end
