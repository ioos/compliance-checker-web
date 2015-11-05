"use strict";
/*
 * cchecker_web/static/js/views/UserLoginFormView.js
 */

var UserLoginFormView = Backbone.View.extend({
  bindings: {
    '#username' : 'login',
    '#password' : 'password'
  },
  events: {
    'click #login' : 'onLogin',
    'click #forgot': 'onForgot'
  },
  onLogin: function(e) {
    e.preventDefault();
    this.trigger('login', this.model);
  },
  onForgot: function(e) {
    e.preventDefault();
    this.trigger('forgot');
  },
  initialize: function(options) {
    _.bindAll(this, "onLogin", "onForgot");
  },
  setAlert: function(message) {
    this.$el.find('#user-alert p').html(message);
    this.$el.find('#user-alert').show();
  },
  template: JST['cchecker_web/static/js/partials/UserLoginForm.html'],
  render: function() {
    this.$el.html(this.template());
    this.stickit();
  }
});
