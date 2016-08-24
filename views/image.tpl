% include('header.tpl')
    <div class="container theme-showcase" role="main">
      <div class="row">
        <div class="col-xs-12">
 	   <h2> Captured Image on {{data['time']}}</h2>

          <div class="row">
		<img class="img-responsive" src="/public/images/{{data['path']}}">
          </div>
          <div class="row">
           <a href="/images"><button type="button" class="btn btn-success">Go back to captured list</button></a>
           <a href="/image/delete/{{data['id']}}/{{data['path']}}"><button type="button" class="btn btn-danger">Delete</button></a>
          </div>
        </div>
      </div>


    </div> <!-- /container -->

% include('footer.tpl')


