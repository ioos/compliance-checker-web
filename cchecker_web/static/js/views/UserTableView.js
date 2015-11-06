"use strict";
/*
 * cchecker_web/static/js/views/UserTableView.js
 */

var UserTableView = Backbone.View.extend({
  views: [],
  template: JST['cchecker_web/static/js/partials/UserTable.html'],
  add: function(model) {
    var self = this;
    var subview = new UserTableItemView({model: model}).render();
    this.$el.find('tbody').append(subview.el);
    this.views.push(subview);
  },
  render: function() {
    var self = this;
    this.$el.html(this.template());
    this.collection.each(function(model) {
      self.add(model);
    });
    return this;
  }
});

var UserTableItemView = Backbone.View.extend({
  tagName: "tr",
  template: JST['cchecker_web/static/js/partials/UserTableItem.html'],
  events: {
    'click' : 'onEdit'
  },
  initialize: function(options) {
    _.bindAll(this, 'onEdit');
  },
  onEdit: function(e) {
    e.preventDefault();
    window.location = this.getEdit();
  },
  getEdit: function() {
    var edit_url = '/user/edit/' + this.model.get('user_id');
    return edit_url;
  },
  render: function() {
    var edit_url = this.getEdit();
    this.$el.html(this.template({model: this.model, edit_url: edit_url}));
    return this;
  }
});
