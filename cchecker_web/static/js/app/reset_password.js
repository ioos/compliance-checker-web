"use strict";
/*
 * cchecker_web/static/js/app/reset_password.js
 */

_.extend(App.prototype, {
  models: {
    userModel: new UserModel()
  },
  views: {
    userChangePasswordFormView: null
  },
  collections: {
  },
  csrf_token: $('meta[name=csrf-token]').attr('content'),
  initializeModels: function() {
    var self = this;
    this.models.userModel.set({
      user_id: user_id,
      password_old: password_token,
      temporary_key: temporary_key
    });
  },
  initializeViews: function() {
    var self = this;

    this.views.userChangePasswordFormView = new UserChangePasswordFormView({
      model: this.models.userModel,
      el: $('#user-password-reset-view')
    });
    this.views.userChangePasswordFormView.render();
  },
  initializeCollections: function() {
    var self = this;
  },
  initializeListeners: function() {
    var self = this;

    this.listenTo(this.views.userChangePasswordFormView, 'submit', function(model) {
      model.changePassword({
        beforeSend: self.beforeSend.bind(self),
        success: function() {
          var path = window.location.href.split('/');
          var url = path.slice(0, path.length-3).join('/');
          window.location = url;
        },
        error: function(jqXHR, textStatus, error) {
          console.error(jqXHR);
        }
      });
    });
  },
  fetchCollections: function() {
    var self = this;
  },
  beforeSend: function(xhr, settings) {
    settings.url = this.urlRoot + settings.url.substring(1, settings.url.length);
    xhr.setRequestHeader("X-CSRFToken", this.csrf_token);
  },
  test: function() {
    var self = this;
  }
});

var app = new App();



