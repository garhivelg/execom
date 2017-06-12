var gulp = require('gulp')
var pug = require('gulp-pug')
var concat = require('gulp-concat')
var less = require('gulp-less')
var csso = require('gulp-csso')
var del = require('del')

gulp.task('clean', function() {
  return del.sync(['static', 'templates']);
});

gulp.task('bootstrap_css', function(){
  return gulp.src([
    'assets/bower_components/bootstrap/dist/css/bootstrap.min.css',
    'assets/bower_components/bootstrap/dist/css/bootstrap-theme.min.css'
  ])
    .pipe(gulp.dest('static/css'));
});

gulp.task('bootstrap_js', function(){
  return gulp.src('assets/bower_components/bootstrap/dist/js/bootstrap.min.js')
    .pipe(gulp.dest('static/js'));
});

gulp.task('bootstrap_fonts', function(){
  return gulp.src('assets/bower_components/bootstrap/dist/fonts/*')
    .pipe(gulp.dest('static/fonts'));
});

gulp.task('jquery', function(){
  return gulp.src('assets/bower_components/jquery/dist/jquery.min.js')
    .pipe(gulp.dest('static/js'));
});

gulp.task('dropzone_css', function(){
  return gulp.src('assets/bower_components/dropzone/dist/min/dropzone.min.css')
    .pipe(gulp.dest('static/css'));
});

gulp.task('dropzone_js', function(){
  return gulp.src('assets/bower_components/dropzone/dist/min/dropzone.min.js')
    .pipe(gulp.dest('static/js'));
});

gulp.task('fa_css', function(){
  return gulp.src('assets/bower_components/components-font-awesome/css/font-awesome.min.css')
    .pipe(gulp.dest('static/css'));
});

gulp.task('fa_fonts', function(){
  return gulp.src('assets/bower_components/components-font-awesome/fonts/*')
    .pipe(gulp.dest('static/fonts'));
});

gulp.task('favicon', function(){
  return gulp.src('assets/favicon/*')
    .pipe(gulp.dest('static/favicon'));
});

gulp.task('fonts', ['bootstrap_fonts', 'fa_fonts']);

// Prepare css
gulp.task('css', ['bootstrap_css', 'dropzone_css', 'fa_css'], function(){
  return gulp.src('assets/css/*.less')
    .pipe(less())
    .pipe(csso())
    .pipe(gulp.dest('static/css'));
});

// Prepare pug
gulp.task('html', function(){
  return gulp.src([
    'assets/pug/*.pug',
    '!assets/pug/_*.pug'
  ])
    .pipe(pug({pretty: true}))
    // .pipe(on("error", console.log))
    .pipe(gulp.dest('templates'));
});

// Prepare js
gulp.task('js', ['jquery', 'bootstrap_js', 'dropzone_js'], function(){
  return gulp.src('assets/js/**/*.js')
    .pipe(concat('index.js'))
    .pipe(gulp.dest('static/js'));
});

// Watch for changes
gulp.task('watch', ['fonts', 'css', 'html', 'js'], function() {
  gulp.watch('assets/css/*.less', ['css']);
  gulp.watch('assets/pug/*.pug', ['html']);
  gulp.watch('assets/js/**/*.js', ['js']);
});

gulp.task('bootstrap', ['bootstrap_css', 'bootstrap_js', 'bootstrap_fonts']);
gulp.task('dropzone', ['dropzone_css', 'dropzone_js']);
gulp.task('fa', ['fa_css', 'fa_fonts']);
gulp.task('default', ['clean', 'favicon', 'fonts', 'html', 'css', 'js']);
