var browserify = require('browserify');
var gulp       = require('gulp');
var clean      = require('gulp-clean');
var source     = require('vinyl-source-stream');

var paths = {
	kernel: './kernel',
	client: './client',
	clientApp: './client/app',
	clientDist: './client/dist',
	clientAssets: [
		'./client/app/img/**/*.*',
		'./client/app/css/**/*.*',
		'./client/app/index.html'
	]
};

gulp.task('clean', function() {
	return gulp.src(paths.clientDist, {read: false})
		.pipe(clean());
});

gulp.task('browserify', function() {
	return browserify(paths.clientApp + "/js/app.js")
		.bundle()
		.pipe(source('main.js'))
		.pipe(gulp.dest(paths.clientDist));
});

gulp.task('copy-assets', function() {
	return gulp.src(paths.clientAssets, {base: paths.clientApp})
		.pipe(gulp.dest(paths.clientDist));
});

gulp.task('default', ['clean'], function() {
	gulp.start('browserify', 'copy-assets');
});
