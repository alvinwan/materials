/**
 * Piazza Poster for Homework
 * --------------------------
 *
 * The following posts the series of images for a homework, to Piazza. You must
 * have a configuration file setup. The configuration file is a JSON which
 * contains the following fields:
 *      username
 *      password
 *      title - accepts two numbers, homework no. and problem no. respectively
 *      body - accepts one string, the image uri
 *
 * Required packages:
 *      piazza-api
 *      imgur
 *      sleep
 *
 * Usage:
 *      node piazza.js <config> n=<homework>
 *
 * Example:
 *      node piazza.js ./config.json n=01
 *
 * @author: Alvin Wan
 * @site: alvinwan.com
 */


var P = require('piazza-api');
var fs = require('fs');
var imgur = require('imgur');
var sleep = require('sleep');
var util = require('util');

var config = JSON.parse(fs.readFileSync(process.argv[2]))

HW = process.argv[3].split('=')[1]
PATH = util.format('./rendered/hw%s/', HW)

P.login(config['email'], config['password']).then(function(user) {
    console.log(' * [INFO] Logged in successfully.')

    fs.readdir(PATH, (err, files) => {

        files = files.map(function(file) { return PATH + file })
             .filter(function(file) { return file.endsWith('png') })
        console.log(' * [INFO] %d files detected.', files.length)

        imgur.uploadImages(files, 'File')
        .then(function (json) {
            console.log(' * [INFO] Images uploaded.')
            uris = json.map(function(image) { image.link })

            for (var i = 1; i < uris.length + 1; i++) {
                uri = uris[i];

                post_title = util.format(config['title'], HW, i)
                post_content = util.format(config['body'], uri)
                user.postNote(config['piazza-course-id'], post_title, post_content, {})

                console.log(' * [INFO] Posted', post_title, ' (sleeping for 2s)')
                sleep.sleep(2)
            }
        })
        .catch(function (err) {
            console.error(err.message);
        });
    })
});