/*
 * cchecker_web/static/js/app/report.js
 */

_.extend(App.prototype, {
  models: {
    report: new ReportModel()
  },
  views: {
    report: null
  },
  initializeViews: function() {
    var self = this;
    this.views.report = new ReportView({
      model: this.models.report,
      el: $('#report')
    });
  },
  initializeModels: function() {
    var self = this;
    var pathArray = window.location.pathname.split('/');
    var jobID = pathArray[pathArray.length - 1];
    this.models.report.set('id', jobID);
    this.models.report.fetch({
      beforeSend: this.beforeSend.bind(this),
      success: function() {
        self.views.report.render();
      },
      error: function() {
        console.error("No job");
      }
    });
  }
});
