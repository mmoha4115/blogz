function loadData() {

  var $body = $('body');
  var $wikiElem = $('#wikipedia-links');
  var $nytHeaderElem = $('#nytimes-header');
  var $nytElem = $('#nytimes-articles');
  var $greeting = $('#greeting');
  var $city = $('#city').val();
  var $street = $('#street').val();
  var address = ''+$street+','+ $city+'';
// google street view api
  $greeting.text('So you want to live at '+address);
  var sig = 'BAwytdnPPWjLSzuOyDJMN37WF6c=';
  var key = 'AIzaSyDAhXzmx1PMU7WOLfDUdTF3asXEDmBWXs0';
  var url ='http://maps.googleapis.com/maps/api/streetview?size=600x300&location='+address+'&key=AIzaSyDAhXzmx1PMU7WOLfDUdTF3asXEDmBWXs0 ';
  $('body').append("<img class ='bgimg' src='"+url+"'>");
  // clear out old data before new request
  $wikiElem.text("");
  $nytElem.text("");
// ny times api - article search
 var page = 0;
  function nytime(page){
    var url = "https://api.nytimes.com/svc/search/v2/articlesearch.json";
  url += '?' + $.param({
    'api-key': "f03475944ea54779981234dbda3ee235",
    'q': address,
    'page': page
  });
  $.getJSON(url).done(function(result) {
    $nytHeaderElem.text("New York articles about " +$city);
    $.each( result.response.docs, function( key, val ) {
    $($nytElem).append("<li id='" + 'article' + "'>" +"<a href='"+ val.web_url+"'>"+ val.headline.main + "</a><p >" + val.snippet + "</p></li>");
    });      
    }).fail(function(err) {    
    $nytHeaderElem.text("There was an error and nytimes articles could not be loaded.");
    throw err;
    });
  }
nytime(page);
//  wiki search links
function wiki(){
  var url = "https://en.wikipedia.org/w/api.php";
url += '?' + $.param({
  'action': 'opensearch',
  'format': 'json',
  'search':$city,
});
var wikiErrorHandling = setTimeout(function(){
  $wikiElem.text("Failed to ger wikipedia search");
},10000);
$.ajax({
  url: url,
  method: 'GET',
  dataType: 'jsonp',
}).done(function(result) {
  var count = 0;
  while (count < result[1].length) {
  $($wikiElem).append("<li><a href='"+result[3][count] +"'>"+ result[1][count] + "</a></li>");
  count++;
  }; clearTimeout(wikiErrorHandling);    
  });
}
wiki();

return false;
};

$('#form-container').submit(loadData);
