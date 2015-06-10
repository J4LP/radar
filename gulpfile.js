var gulp = require('gulp');
var sourcemaps = require('gulp-sourcemaps');
var bower = require('bower-files')();
var concat = require('gulp-concat');
var typescript = require('gulp-typescript');
var less = require('gulp-less');
var uglify = require('gulp-uglify');
var nodemon = require('gulp-nodemon');
var browserSync = require('browser-sync');
var reload = browserSync.reload;
var yaml = require('js-yaml');
var fs = require('fs');
var template = require('gulp-template');

var config = {
  API_ROOT: '/api'
};

try {
  config = yaml.safeLoad(fs.readFileSync('./config.yml', 'utf-8'));
} catch(e) {
  console.log(e);
}

var paths = {
  'scripts': ['./radar/static/scripts/**/*.ts'],
  'templates': ['./radar/templates/**/*.html'],
  'styles': ['./radar/static/styles/**/*.less']
};

gulp.task('less', function() {
  return gulp.src(paths.styles)
    .pipe(sourcemaps.init())
    .pipe(less())
    .pipe(concat('style.css'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('./radar/public/styles/'))
    .pipe(reload({stream: true}))
});

gulp.task('bowerdeps', function() {
  return gulp.src(bower.ext('js').files)
    .pipe(sourcemaps.init())
    .pipe(concat('libs.min.js'))
    .pipe(uglify())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('./radar/public/scripts/'))
});

var clientProject = typescript.createProject({
  module: 'amd',
  declarationFiles: false,
  sortOutput: true
});

gulp.task('typescript', function() {
  gulp.src(paths.scripts)
      .pipe(template(config))
    .pipe(sourcemaps.init())
    .pipe(typescript(clientProject).js)
    .pipe(concat('application.js'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('./radar/public/scripts/'));
  reload()
});


gulp.task('watch', ['typescript', 'less'], function() {

  //nodemon({
  //  exec: 'python run.py',
  //  watch: ['**/*.py']
  //})

  browserSync({
    proxy: '127.0.0.1:5002',
    files: ['public/**/*.{js,css}']
  });

  gulp.watch(paths.scripts, ['typescript']);
  gulp.watch(paths.styles, ['less']);
  gulp.watch(paths.templates, reload)
});

gulp.task('default', ['typescript', 'less', 'bowerdeps']);
