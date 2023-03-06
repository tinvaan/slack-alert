# frozen_string_literal: true

class BounceController < ApplicationController
  def notify
    record = JSON.parse(request.body.read)

    if record['RecordType'] == 'Bounce'
      if record['Type'] == 'SpamNotification' && record['TypeCode'] == 512
        return SlackNotifyJob.set(queue: :spam).perform_later(record)
      end

      return [{
        'Type': record['Type'],
        'Email': record['Email'],
        'BouncedAt': record['BouncedAt'],
        'Description': record['Description'],
        'Tag': record['Tag']
      }, 200]
    end

    [{ 'error': 'Bad Request' }, 400]
  end
end
