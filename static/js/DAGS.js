$(document).ready(function() {
TreeMenu();

});

function TreeMenu(){

    //$('body').prepend('<div id="MenuDiv" class="MenuDiv">Navigation</div>');
    //$('#MenuDiv').css('visibility','show');

    $('<a></a>').text('Go Back To Top').attr({'title': 'Go Top', 
					      'href': '#tableofcontents',
					      'class': 'goback'}).appendTo('#content');
    $('a.goback').bind('click', SmoothScroll);   

    $('div#content h1').each(function(i){
    //Get each h1's text for title
    var sectionObj = $(this);
    var chapterTitle = sectionObj.text();
    // section id
    var chapterId = 'section' + (i + 1);
	
    //Attach id to sections to handle internal page link
    sectionObj.attr('id', chapterId);

    $('<div></div>').attr({'id': 'title' + i}).appendTo('#tableofcontents');

    $('<a></a>').text(chapterTitle).attr({'title': 'View' + chapterTitle, 
				    'href': '#' + chapterId,
  				    'class': 'indexlink'
				  }).appendTo('#tableofcontents');
    });

    $('a.indexlink').bind('click', SmoothScroll); 

    function SmoothScroll(){
        
        var targetName = $(this).attr('href');
        var targetObj = $(targetName);
	var distance = targetObj.offset().top;
        var timer = 1000;

        $('html,body').animate({scrollTop: distance}, timer);
	return false;
    }



};
