% include('header.tpl')
    <div class="container theme-showcase" role="main">
      <div class="row">
      	<div class="col-md-4"></div>
  	<div class="col-md-4">
		<img class="img-responsive" src="/public/images/ansakit.jpg" alt="">
	</div>
 	<div class="col-md-4"></div>
      </div>
      <div class="row">
          <table class="table table-hover">
              <thead>
                 <tr>
			<th> Time </th>
                 	<th> Type </th>
                 	<th> Notes </th>
		</tr>
              </thead>
              <tbody>
                 % for x in data:
                 <tr>
			<td> {{x['time']}} </td>
                 	<td> {{x['type']}} </td>
                 	<td> {{x['note']}} </td>
		</tr>
                % end
              </tbody>
       
          </table>
      </div>


    </div> <!-- /container -->

% include('footer.tpl')


