"use strict"
/*
 * cchecker_web/static/js/app/NewUser.js
 */

_.extend(App.prototype, {
  models: {
    userModel: new UserModel()
  },
  views: {
    navbar: null,
    userFormView: null
  },
  collections: {},
  csrf_token: $('meta[name=csrf-token]').attr('content'),
  initializeModels: function() {
    var self = this;
  },
  initializeViews: function() {
    var self = this;

    this.views.navbar = new IOOSNavbarView({
      el: $('#navbar-view'),
      links: [{
        name: "Login",
        href: this.urlRoot + "user/login"
      }]
    }).render();

    this.views.userFormView = new UserFormView({
      legend: "New User Account",
      el: $('#user-form-view'),
      model: this.models.userModel
    });
    this.views.userFormView.render();
  },
  initializeCollections: function() {
    var self = this;
  },
  initializeListeners: function() {
    var self = this;

    this.listenTo(this.views.userFormView, 'submit', function(model) {
      // Save the form
      // If the form saved, log the user in
      // if that worked then redirect
      model.save({},{
          beforeSend: self.beforeSend.bind(self),
          success: function(model, response, options) {
            model.login({
              beforeSend: self.beforeSend.bind(self),
              success: function(data, textStatus, jqXHR) {
                window.location.href = app.urlRoot;
              },
              error: function(jqXHR, textStatus, options) {
                self.views.userFormView.setAlert(jqXHR.responseJSON.message);
              }
            });
          },
          error: function(model, response, options) {
            self.views.userFormView.setAlert(response.responseJSON.message);
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

