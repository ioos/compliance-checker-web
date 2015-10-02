module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    assets: grunt.file.readJSON('Assets.json'),
    jst: {
      compile: {
        files: '<%= assets.main.jst %>'
      }
    },
    uglify: {
      main: {
        options: {
          mangle: false,
          compress: false,
          beautify: true
        },
        files: '<%= assets.main.js %>'
      }
    },
    cssmin: {
      main: {
        files: '<%= assets.main.css %>'
      }
    },
    watch: {
      partials: {
        files: ['Assets.json', 'Gruntfile.js', '**/partials/*.html'],
        tasks: ['jst'],
        options: {
        }
      }
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jst');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default', ['jst', 'cssmin', 'uglify']);
  // Empty Commnet
};

