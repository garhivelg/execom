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

gulp.task('chart', function(){
  return gulp.src('assets/bower_components/chart.js/dist/Chart.min.js')
    .pipe(gulp.dest('static/js'));
});

gulp.task('jquery', function(){
  return gulp.src('assets/bower_components/jquery/dist/jquery.min.js')
    .pipe(gulp.dest('static/js'));
});

gulp.task('pace', function(){
  return gulp.src('assets/bower_components/PACE/pace.min.js')
    .pipe(gulp.dest('static/js'));
});

gulp.task('tether', function(){
  return gulp.src('assets/bower_components/tether/dist/js/tether.min.js')
    .pipe(gulp.dest('static/js'));
});

gulp.task('crud_css', function(){
  return gulp.src([
    'assets/bower_components/crud-assets/css/main.less'
  ])
    .pipe(gulp.dest('assets/less'));
});

gulp.task('crud_js', function(){
  return gulp.src('assets/bower_components/crud-assets/js/**/*.js')
    .pipe(gulp.dest('assets/js/crud-assets'));
});

// Prepare css
gulp.task('less', ['crud_css', ], function(){
  return gulp.src('assets/less/*.less')
    .pipe(less())
    .pipe(concat('index.css'))
    // .pipe(csso())
    .pipe(gulp.dest('static/css'));
});

gulp.task('css', ['bootstrap_css', 'less'], function(){
  return gulp.src('assets/css/*.css')
    .pipe(csso())
    .pipe(gulp.dest('static/css'));
});

gulp.task('favicon', function(){
  return gulp.src('assets/favicon/*')
    .pipe(gulp.dest('static/favicon'));
});

// Prepare fonts
gulp.task('fonts', ['bootstrap_fonts'], function(){
  return gulp.src('assets/fonts/*')
    .pipe(gulp.dest('static/fonts'));
});

gulp.task('img', function(){
  return gulp.src('assets/img/*')
    .pipe(gulp.dest('static/img'));
});

//Prepare images
gulp.task('images', ['img'], function(){
return gulp.src('assets/images/*')
 .pipe(gulp.dest('static/images'));
});

// Prepare js
gulp.task('js', ['jquery', 'bootstrap_js', 'crud_js', 'tether', 'pace', 'chart'], function(){
  return gulp.src([
    'assets/js/**/*.js',
    '!assets/js/views/*.js'
  ])
    .pipe(concat('index.js'))
    .pipe(gulp.dest('static/js'));
});

// Prepare pug
gulp.task('txt', function(){
  return gulp.src([
    'assets/templates/**/*.txt',
    '!assets/templates/**/_*.txt'
  ])
    .pipe(gulp.dest('templates/'));
});

gulp.task('html', ['txt'], function(){
  return gulp.src([
    'assets/templates/**/*.pug',
    '!assets/templates/**/_*.pug'
  ])
    .pipe(pug({pretty: true}))
    // .pipe(on("error", console.log))
    .pipe(gulp.dest('templates/'));
});

// Watch for changes
gulp.task('watch', ['css', 'html', 'js', 'fonts', 'images'], function() {
  gulp.watch('assets/less/*.less', ['css']);
  gulp.watch('assets/templates/**/*.pug', ['html']);
  gulp.watch('assets/fonts/*', ['fonts']);
  gulp.watch('assets/js/**/*.js', ['js']);
  gulp.watch('assets/images/*', ['images']);
});

gulp.task('bootstrap', ['bootstrap_css', 'bootstrap_js', 'bootstrap_fonts']);
gulp.task('dropzone', ['dropzone_css', 'dropzone_js']);
gulp.task('default', ['clean', 'favicon', 'fonts', 'html', 'css', 'js', 'images']);
