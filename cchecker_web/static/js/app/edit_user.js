"use strict"
/*
 * cchecker_web/static/js/app/EditUser.js
 */

_.extend(App.prototype, {
  models: {
    userModel: new UserModel()
  },
  views: {
    userFormView: null
  },
  collections: {},
  csrf_token: $('meta[name=csrf-token]').attr('content'),
  initializeModels: function() {
    var self = this;
    var pathArray = window.location.pathname.split('/');
    var userID = pathArray[pathArray.length-1];

    this.models.userModel.set('user_id', userID);

  },
  initializeViews: function() {
    var self = this;

    this.views.userFormView = new UserFormView({
      legend: "Edit User Account",
      type: UserFormView.EDIT_ACCOUNT,
      el: $('#user-form-view'),
      model: this.models.userModel
    });
    $.when(this.models.userModel.fetch()).done(function() {
      self.views.userFormView.render();
    });
  },
  initializeCollections: function() {
    var self = this;
  },
  initializeListeners: function() {
    var self = this;

    this.listenTo(this.views.userFormView, 'submit', function(model) {
      model.save({},{
          beforeSend: self.beforeSend.bind(self),
          success: function(model, response, options) {
            if(document.referrer != document.location.href) {
              window.location = document.referrer;
            }
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
  beforeSend: function(xhr) {
    xhr.setRequestHeader("X-CSRFToken", this.csrf_token);
  },
  test: function() {

  }
});

var app = new App();



