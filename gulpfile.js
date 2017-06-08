var gulp = require('gulp')
var pug = require('gulp-pug')
var less = require('gulp-less')
var csso = require('gulp-csso')

gulp.task('bootstrap_css', function(){
  return gulp.src([
    'assets/bower_components/bootstrap/dist/css/bootstrap.min.css',
    'assets/bower_components/bootstrap/dist/css/bootstrap-theme.min.css'
  ])
    .pipe(gulp.dest('static/css'))
});

gulp.task('bootstrap_js', function(){
  return gulp.src('assets/bower_components/bootstrap/dist/js/bootstrap.min.js')
    .pipe(gulp.dest('static/js'))
});

gulp.task('bootstrap_fonts', function(){
  return gulp.src('assets/bower_components/bootstrap/dist/fonts/*')
    .pipe(gulp.dest('static/fonts'))
});

gulp.task('jquery', function(){
  return gulp.src('assets/bower_components/jquery/dist/jquery.min.js')
    .pipe(gulp.dest('static/js'))
});

gulp.task('dropzone_css', function(){
  return gulp.src('assets/bower_components/dropzone/dist/min/dropzone.min.css')
    .pipe(gulp.dest('static/css'))
});

gulp.task('dropzone_js', function(){
  return gulp.src('assets/bower_components/dropzone/dist/min/dropzone.min.js')
    .pipe(gulp.dest('static/js'))
});

gulp.task('favicon', function(){
  return gulp.src('assets/favicon/*')
    .pipe(gulp.dest('static/favicon'))
});

gulp.task('html', function(){
  return gulp.src('assets/pug/*.pug')
    .pipe(pug())
    .pipe(gulp.dest('templates'))
});

gulp.task('css', function(){
  return gulp.src('assets/css/*.less')
    .pipe(less())
    .pipe(csso())
    .pipe(gulp.dest('static/css'))
});

gulp.task('bootstrap', ['bootstrap_css', 'bootstrap_js', 'bootstrap_fonts']);
gulp.task('dropzone', ['dropzone_css', 'dropzone_js']);
gulp.task('default', ['favicon', 'html', 'css', 'jquery', 'bootstrap', 'dropzone']);
