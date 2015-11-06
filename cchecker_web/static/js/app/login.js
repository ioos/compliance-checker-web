"use strict"
/*
 * cchecker_web/static/js/app/EditUser.js
 */

_.extend(App.prototype, {
  models: {
    userModel: new UserModel()
  },
  views: {
    navbar: null,
    userLoginFormView: null,
    userPasswordResetFormView: null
  },
  collections: {},
  csrf_token: $('meta[name=csrf-token]').attr('content'),
  initializeModels: function() {
    var self = this;
    this.models.userModel.set({user_id: "self"});
    this.models.userModel.fetch({
      success: function(model, response, options) {
        window.location.href = '/';
      },
      error: function(model, response, options) {
        self.initializeViews();
        self.initializeListeners();
      }
    });
  },
  initializeViews: function() {
    var self = this;

    this.views.navbar = new IOOSNavbarView({
      el: $('#navbar-view'),
      links: []
    });
    this.views.navbar.render();

    // See if we're logged in already. If we aren't then present the form

    this.views.userLoginFormView = new UserLoginFormView({
      el: $('#user-login-view'),
      model: this.models.userModel
    });
    this.views.userLoginFormView.render();
    this.views.userPasswordResetFormView = new UserPasswordResetFormView({
      el: $('#user-password-reset-view'),
      model: this.models.userModel
    });
    this.views.userPasswordResetFormView.$el.hide();
    this.views.userPasswordResetFormView.render();
  },
  initializeCollections: function() {
    var self = this;
  },
  initializeListeners: function() {
    var self = this;

    this.listenTo(this.views.userLoginFormView, "login", function(model) {
      model.login({
        beforeSend: self.beforeSend.bind(self),
        success: function(data, textStatus, jqXHR) {
          window.location.href = '/';
        },
        error: function(jqXHR, textStatus, response) {
          self.views.userLoginFormView.setAlert(jqXHR.responseJSON.message);
        }
      });
    });
    this.listenTo(this.views.userLoginFormView, "forgot", function() {
      self.views.userLoginFormView.$el.hide();
      self.views.userPasswordResetFormView.$el.show();
    });
    this.listenTo(this.views.userPasswordResetFormView, 'back', function() {
      self.views.userPasswordResetFormView.$el.hide();
      self.views.userLoginFormView.$el.show();
    });
    this.listenTo(this.views.userPasswordResetFormView, 'passwordReset', function(model) {
      $('#user-password-reset-view').hide();
      $('.login-content').html('<i class="fa fa-spinner fa-spin" style="margin-top:140px;margin-left:40%;font-size:90px;"> </i>')
      model.resetPassword({
        beforeSend: self.beforeSend.bind(self),
        success: function(data, textStatus, jqXHR) {
          $('.login-content').html('<div class="alert alert-success">Email Sent. Password reset instructions should be in your email shortly.</div>');
          setTimeout(function() {
            window.location.href='/';
          }, 5000);
        },
        error: function(jqXHR, textStatus, error) {
          $('.login-content').html('<div class="alert alert-danger">' + jqXHR.responseJSON.message + '</div>');
          setTimeout(function() { 
            window.history.back();
          }, 3000);
        }
      });
    });
    this.listenTo(this.views.userLoginFormView, "register", function(e) {
      window.location.href = self.urlRoot + "user/new";
    });
  },
  fetchCollections: function() {
    var self = this;
  },
  beforeSend: function(xhr) {
    xhr.setRequestHeader("X-CSRFToken", this.csrf_token);
  },
  start: function() {
    this.initializeModels();
    this.initializeCollections();
    this.fetchCollections();
  }

});

var app = new App();

