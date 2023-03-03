# frozen_string_literal: true

Rails.application.routes.draw do
  post "alert/bounced" => "Bounce#notify"
end
