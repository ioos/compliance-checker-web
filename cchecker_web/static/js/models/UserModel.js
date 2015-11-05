"use strict";
/*
 * cchecker_web/static/js/models/UserModel.js
 *
 * Model to define the User
 */

var UserModel = Backbone.Model.extend({
  urlRoot: "/api/user/",
  idAttribute: 'user_id',
  defaults: {
    first_name: "",
    last_name: "",
    email: "",
    login: "",
    password: "",
    password_confirm: "",
    permissions: {}
  },
  validate: function() {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    
    if(this.get("first_name").length < 1) {
      return "First Name can't be empty";
    }
    if(this.get("last_name").length < 1) {
      return "Last name can't be empty";
    }
    if(this.get("email").length < 1) {
      return "Email can't be empty";
    }
    if(this.get('login').length < 1) {
      return "Username can't be empty";
    }
    if(!re.test(this.get('email'))) {
      return "Not a valid email address";
    }
    if(this.get('password') != this.get('password_confirm')) {
      return "Passwords do not match";
    }
  },
  login: function(options) {
    var self = this;
    var ajaxOpts = _.extend({
      url: "/api/user/login",
      type: 'POST',
      dataType: 'json',
      contentType: "application/json",
      data: JSON.stringify({login: this.get('login'), password: this.get('password')}),
      success: function(data, textStatus, jqXHR) {
        self.set({
          user_id: data.user_id
        });
          
        if(options && options.success) {
          options.success(arguments);
        }
      }
    }, options);
    return $.ajax(ajaxOpts);
  },
  changePassword: function(options) {
    var self = this;
    var ajaxOpts = _.extend({
      url: "/api/user/change_password",
      type: 'POST',
      dataType: 'json',
      contentType: "application/json",
      data: JSON.stringify({
        user_id: this.get('user_id'), 
        password: this.get('password'),
        password_old: this.get('password_old'),
        temporary_key: this.get('temporary_key')
      })
    }, options);
    return $.ajax(ajaxOpts);
  },
  resetPassword: function(options) {
    var self = this;
    var ajaxOpts = _.extend({
      url: "/api/user/reset",
      type: 'POST',
      dataType: 'json',
      contentType: "application/json",
      data: JSON.stringify({
        email: this.get('email')
      })
    }, options);
    return $.ajax(ajaxOpts);
  }
});

var UserCollection = Backbone.Collection.extend({
  url: '/api/user',
  model: UserModel,
  parse: function(response) {
    if(response && response.items) {
      return response.items;
    }
  }
});
