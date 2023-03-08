# frozen_string_literal: true

class BounceController < ApplicationController
  before_action :parse, only: [:notify]

  def notify
    if @record && @record['RecordType'] == 'Bounce'
      if @record['Type'] == 'SpamNotification' && @record['TypeCode'] == 512
        return SlackNotifyJob.set(queue: :spam).perform_now(@record) # TODO: perform_later
      end

      return render status: 200, json: {
        'Type': @record['Type'],
        'Email': @record['Email'],
        'BouncedAt': @record['BouncedAt'],
        'Description': @record['Description'],
        'Tag': @record['Tag']
      }
    end

    return render status: 400, json: { 'error': 'Bad Request' }
  end

  private

  def parse
    @record = JSON.parse(request.body.read)
  rescue JSON::ParserError => e
    print("\nFailed to parse request payload, #{request.body.read}")
    print("\nException: #{e}")

    @record = nil
  end
end
