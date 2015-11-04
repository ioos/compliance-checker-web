/*
 * cchecker_web/static/js/views/NetCDFUploadView.js
 *
 * A simple icon and filename for the netCDF upload
 */

var NetCDFUploadView = Backbone.View.extend({
  initialize: function(options) {
  },
  template: JST['cchecker_web/static/js/partials/NetCDFUpload.html'],
  render: function() {
    this.$el.html(this.template({model: this.model}));
  }
});


