/*
 * cchecker_web/static/js/app/report.js
 */

_.extend(App.prototype, {
  models: {
    report: new ReportModel(),
    references: new ReferencesModel()
  },
  views: {
    report: null,
    navbar: null,
  },
  initializeViews: function() {
    var self = this;
    this.views.report = new ReportView({
      model: this.models.report,
      el: $('#report')
    });

    var referenceUrls = _.compact(this.models.references.get('references'));

    // Initialize the Navbar with a Logout button
    this.views.navbar = new IOOSNavbarView({
      el: $('#navbar-view'),
      referenceUrls: referenceUrls,
      page: 'report',
    });

    this.views.navbar.render();
  },
  initializeModels: function() {
    var self = this;
    var pathArray = window.location.pathname.split('/');
    var jobID = pathArray[pathArray.length - 1];
    this.models.report.set('id', jobID);
    var reportUrl = this.urlRoot + 'api/download?id=' + this.models.report.get('id');
    this.models.report.set('reportUrl', reportUrl);

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
