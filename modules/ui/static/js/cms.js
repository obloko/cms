$(function() {
    $('#side-menu').metisMenu();

});

function cleanUrl(url) {
	  str = ""+url;
	  return str.split("?")[0].split("#")[0];
	}

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    var url = window.location;
    var element = $('ul.nav a').filter(function() {
        return this.href == url || url.href.indexOf(this.href) == 0;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }
    
    var tabelement = $('ul.dynotabs a').filter(function() {
    	return this.href == url;
    }).parent().addClass('active');
});
