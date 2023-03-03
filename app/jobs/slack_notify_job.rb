# frozen_string_literal: true

require 'slack-ruby-client'


class SlackNotifyJob < ApplicationJob
  queue_as :spam

  def perform(*args)
    Slack.configure do |config|
      config.token = ENV['SLACK_BOT_TOKEN']
      raise 'Missing SLACK_BOT_TOKEN!' unless config.token
    end

    client :Slack::Realtime::Client.new
    render :client.chat_postMessage(channel: '#spam', as_user: true, blocks: JSON.dump([
      {
        'type': 'header',
        'text': {
          'type': 'plain_text',
          'text': args[:'Name']
        }
      },
      {
        'type': 'section',
        'fields': [
          {
            'type': 'mrkdwn',
            'text': '*Email:* ' + args[:'Email']
          }
        ]
      },
      {
        'type': 'section',
        'fields': [
          {
            'type': 'mrkdwn',
            'text': '*When:* ' + args[:'BouncedAt']
          }
        ]
      },
      {
        'type': 'section',
        'text': {
          'type': 'mrkdwn',
          'text': '*Description:* ' + args[:'Description']
        }
      }
    ]))
  end

end
