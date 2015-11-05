"use strict"
/*
 * cchecker_web/static/js/views/UserFormView.js
 */

var UserFormView = Backbone.View.extend({
  bindings: {
    '#first_name' : 'first_name',
    '#last_name' : 'last_name',
    '#login':'login',
    '#email' : 'email',
    '#password' : 'password',
    '#password_confirm' : 'password_confirm',
    '#old-password' : 'password_old'
  },
  events: {
    'click #submit' : 'onSubmit',
    'click .close' : 'onAlertClose'
  },
  onAlertClose: function(e) {
    e.preventDefault();
    this.$el.find('#user-alert').hide();
  },
  onSubmit: function(e) {
    e.preventDefault();
    if(!this.model.isValid()) {
      this.setAlert(this.model.validationError);
      return;
    }
    if(this.options.type == UserFormView.NEW_ACCOUNT) {
      this.trigger('submit', this.model);
    } else if(this.model.get('password') == "") {
      this.trigger('submit', this.model);
    } else {
      this.trigger('changePassword', this.model);
    }
  },
  setAlert: function(message) {
    this.$el.find('#user-alert p').html(message);
    this.$el.find('#user-alert').show();
  },
  initialize: function(options) {
    _.bindAll(this, 'onAlertClose', 'onSubmit');
    this.options = _.extend({
      legend: "New User Account",
      type: UserFormView.NEW_ACCOUNT
    }, options);

  },
  template: JST['cchecker_web/static/js/partials/UserForm.html'],
  render: function() {
    this.$el.html(this.template({
      legend: this.options.legend,
      new_account: this.options.type == UserFormView.NEW_ACCOUNT
    }));
    //this.$el.find('#user-alert').hide();
    this.stickit();
    return this;
  },
});

UserFormView.NEW_ACCOUNT    = 1;
UserFormView.EDIT_ACCOUNT   = 2;
