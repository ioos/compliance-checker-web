"use strict"
/*
 * cchecker_web/static/js/views/UserChangePasswordFormView.js
 */

var UserChangePasswordFormView = Backbone.View.extend({
  bindings: {
    '#password' : 'password',
    '#password_confirm' : 'password_confirm'
  },
  events: {
    'click #submit' : 'onSubmit'
  },
  onSubmit: function(e) {
    e.preventDefault();
    if(this.model.get('password') != this.model.get('password_confirm')) {
      this.setAlert("Passwords do not match");
      return;
    }
    this.trigger('submit', this.model);
  },
  setAlert: function(message) {
    this.$el.find('#user-alert p').html(message);
    this.$el.find('#user-alert').show();
  },
  initialize: function(options) {
    this.options = _.extend({
    }, options);

    _.bindAll(this, 'onSubmit');
  },
  template: JST['cchecker_web/static/js/partials/UserChangePasswordForm.html'],
  render: function() {
    this.$el.html(this.template());
    this.stickit();

    return this;
  }
});

