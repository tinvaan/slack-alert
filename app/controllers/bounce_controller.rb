# frozen_string_literal: true

class BounceController < ApplicationController
  def notify
    payload = JSON.parse(request.body.read)
    if payload[:'RecordType'] == 'Bounce'
      if payload[:'Type'] == 'SpamNotification' and payload[:'TypeCode'] == 512
        return render :SlackNotifyJob.perform_later payload

      return render json: {
        'Type': payload[:'Type'],
        'Email': payload[:'Email'],
        'BouncedAt': payload[:'BouncedAt'],
        'Description': payload[:'Description'],
        'Tag': payload[:'Tag']
      }, status: 200

    return render json: {'error': 'Bad Request'}, status: 400
  end
end
