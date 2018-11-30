
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');
    var $city = $('#city').val();
    var $street = $('#street').val();
    var address = ''+$street+','+ $city+'';
    var nydata;
    console.log(address);

    $greeting.text('So you want to live at '+address);
    var sig = 'BAwytdnPPWjLSzuOyDJMN37WF6c=';
    var key = 'AIzaSyDAhXzmx1PMU7WOLfDUdTF3asXEDmBWXs0';
    var url ='http://maps.googleapis.com/maps/api/streetview?size=600x300&location='+address+'&key=AIzaSyDAhXzmx1PMU7WOLfDUdTF3asXEDmBWXs0 ';
    $('body').append("<img class ='bgimg' src='"+url+"'>");

    console.log("should work");

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

   var url2 = "https://api.nytimes.com/svc/search/v2/articlesearch.json";
    url2 += '?' + $.param({
      'api-key': "f03475944ea54779981234dbda3ee235",
      'q': address
    });
    console.log(url2);
    var items = {};
    $.ajax({
      url: url2,
      method: 'GET',
    }).done(function(result) {
      console.log(result,'retult');
       var count=0;
       items = result.response.docs;
       console.log(result.response.docs,'response');
    $.each( result.response.docs, function( key, val ) {
        items+=( "<li id='" + key + "'>" + val.web_url + "</li>" );
        console.log(val.web_url);
        count++;
  });
    }).fail(function(err) {
      throw err;
    });
    console.log(items);
  //   
  //   var count=0;
  //   $.each( nydata, function( key, val ) {
  //   items.push( "<li id='" + key + "'>" + val + "</li>" );
  //   console.log(items[count],'count');
  //   count++;
  //   console.log(items)
  // });

    // YOUR CODE GOES HERE!

    return false;
};

$('#form-container').submit(loadData);
