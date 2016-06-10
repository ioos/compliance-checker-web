"use strict";
/*
 * cchecker_web/static/js/app/index.js
 */

_.extend(App.prototype, {
  views: {
    navbar: null,
    testSelection: null,
    netCDFUpload: null
  },
  collections: {
    testCollection: new TestCollection()
  },
  models:{
    upload: new UploadModel(),
    configModel: new ConfigModel()
  },
  form: new FormData(),
  initializeViews: function() {
    var self = this;
    // Initialize the Navbar with a Logout button
    this.views.navbar = new IOOSNavbarView({
      el: $('#navbar-view')
    });
    this.views.navbar.render();

    this.views.testSelection = new TestSelectionView({
      el: $('.testselection'),
      collection: this.collections.testCollection
    });

    this.views.netCDFUpload = new NetCDFUploadView({
      el: $('#fileupload'),
      model: this.models.upload
    });
  },
  initializeCollections: function() {
    var self = this;

    // Get the checkers
    var testFetch = this.collections.testCollection.fetch({
      beforeSend: this.beforeSend.bind(this)
    });
    $.when.apply($, [testFetch]).done(function() {
      self.views.testSelection.render();
    });
  },
  initializeModels: function() {
    var self = this;
  },
  fetchCollections: function() {
    var self = this;
    var configFetch = this.models.configModel.fetch({
      beforeSend: this.beforeSend.bind(this),
      success: function(model) {
        var size = model.get('size_limit') / 1048576;
        $('#max-size').html("(Max Size: " + size.toFixed(1).toString() + "MB)");
      }
    });
  },
  start: function() {
    var self = this;
    this.drop = $('#dropbox');
    this.submit = $('#submit-btn');

    // Listen for someone selecting a file witht he browse button
    $('.btn-file :file').change(function(e) {
      if($(this).get(0).files.length > 0) {
        var file = $(this).get(0).files[0];
        self.models.upload.set({filename: file.name, file:file});
        self.drop.addClass('uploading');
        self.views.netCDFUpload.render();
      }
    });

    // Someone dragged a file
    this.drop.on('dragover', function(e) {
      e.preventDefault();
      e.stopPropagation();
      $(this).removeClass();
      self.views.netCDFUpload.$el.html("");
    });

    this.drop.on('dragenter', function(e) {
      $(this).addClass('hovered');
    });

    this.drop.on('dragleave', function(e) {
      $(this).removeClass('hovered');
    });

    // Someone dropped a file
    this.drop.on('drop', function(e) {
      e.preventDefault();
      e.stopPropagation();

      _.each(e.originalEvent.dataTransfer.files, function(file, i) {
        if(i > 0) {
          return;
        }
        self.models.upload.set({filename: file.name, file: file});
      });

      $(this).addClass('uploading');
      self.views.netCDFUpload.render();
    });


    this.submit.on('click', function() {
      var checkID = self.views.testSelection.getSelected();
      self.form.append('checker', checkID);
      self.form.append('file-0', self.models.upload.get('file'));
      var urlInput = $('#url-input').val();
      if(urlInput.length > 0) {
        self.form.append('url', urlInput);
      }
      var req = $.ajax({
        url: self.urlRoot + 'upload',
        xhr: function() {
          var x = $.ajaxSettings.xhr();
          x.upload.addEventListener('progress', function(e) {
            if(e.lengthComputable) {
              var pct = e.loaded / e.total * 100;
            }
          }, false);
          return x;
        },
        type: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        data: self.form
      });
      req.always(function() {
        self.drop.removeClass('uploading');
      });
      req.done(function(data) {
        $('.drop-status').html('<div class="alert alert-success"><i class="fa fa-spin fa-fw fa-spinner"> </i>' + data.message + '</div>');
        self.pollResult(data.job_id);
      });
      req.error(function(jqXHR, textStatus, error) {
        if(jqXHR.status == 413) {
          $('.drop-status').html('<div class="alert alert-danger">File is too large!</div>');
        } else if(jqXHR.status == 400) {
          $('.drop-status').html('<div class="alert alert-danger">' + jqXHR.responseJSON.message + '</div>');
        } else {
          $('.drop-status').html('<div class="alert alert-danger">' + error + '</div>');
        }
      });
    });
    this.initializeModels();
    this.initializeCollections();
    this.initializeViews();
    this.initializeListeners();
    this.fetchCollections();
  },
  pollResult: function(jobID, count) {
    var self = this;
    count = count || 0;
    if(count > 120) {
          $('.drop-status').html('<div class="alert alert-danger"><p>Error while processing the job.</p><p>Job Timed Out</p></div>');
          return;
    }
    $.ajax({
      url: '/api/job/' + jobID,
      dataType: 'json',
      method: 'GET',
      beforeSend: this.beforeSend.bind(this),
      success: function() {
        window.location.href = self.urlRoot + 'report/' + jobID;
      },
      error: function(jqXHR, response, options) {
        if(jqXHR.status == 404) {
          setTimeout(function() {
            self.pollResult(jobID, count+1)
          }, 500);
        } else if(jqXHR.status == 400) {
          $('.drop-status').html('<div class="alert alert-danger"><p>Error while processing the job.</p><p>' + jqXHR.responseJSON.error +': ' + jqXHR.responseJSON.message +  '</p></div>');
        } else {
          $('.drop-status').html('<div class="alert alert-danger"><p>Error while processing the job.</p><p>Server Error, please check the logs</p></div>');
        }
      }
    });
  }
});

