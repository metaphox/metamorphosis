/* Author: 

*/

$(document).ready(function(){
	var tightMargin = 4;
	var adjTopNag = 0;
	for(i = 1, count = $('.footnotelist li').size(); i<=count; i++){
		var noteSelector = '#note-'+i;
		var refSelector = '.ref-'+i;
                if(!$(refSelector)[0]) continue;
		var offset = $($(refSelector)[0]).offset().top - $(noteSelector).offset().top - adjTopNag;		
		$(noteSelector).css('margin-top', (offset < 0 ? tightMargin : offset) );
		$(refSelector).hover(function(){
			$('#note-'+$(this).attr('class').match(/ref-(\d*)/)[1]).css({backgroundColor:'#f6f6e6'});
		}, function(){
			$('#note-'+$(this).attr('class').match(/ref-(\d*)/)[1]).css({backgroundColor:'transparent'});
		});
	}
});






















