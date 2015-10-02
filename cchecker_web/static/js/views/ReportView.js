/*
 * cchecker_web/static/js/views/ReportView.js
 */

var ReportView = Backbone.View.extend({
  initialize:function(options) {
  },
  template: JST['cchecker_web/static/js/partials/Report.html'],
  render: function() {
    this.$el.html(this.template({model: this.model}));
    this.$el.find('.high-priority-table').collapse({toggle: false});
    this.$el.find('.table-collapse').click(function(e) {
      e.preventDefault();
      $('.' + $(e.target).data('target')).collapse('toggle');
      var glyph = $(e.target).find('.glyphicon');
      if(glyph.hasClass('glyphicon-collapse-up')) {
        glyph.removeClass('glyphicon-collapse-up');
        glyph.addClass('glyphicon-collapse-down');
      } else {
        glyph.removeClass('glyphicon-collapse-down');
        glyph.addClass('glyphicon-collapse-up');
      }
    });
    this.$el.find('.table-collapse i.glyphicon').click(function(e) {
      e.preventDefault();
      $('.' + $(e.target).data('target')).collapse('toggle');
      var glyph = $(e.target).find('.glyphicon');
      if(glyph.hasClass('glyphicon-collapse-up')) {
        glyph.removeClass('glyphicon-collapse-up');
        glyph.addClass('glyphicon-collapse-down');
      } else {
        glyph.removeClass('glyphicon-collapse-down');
        glyph.addClass('glyphicon-collapse-up');
      }
    });
    return this;
  }
});
