% include('header.tpl')
    <div class="container theme-showcase" role="main">
      <div class="row">
      	<div class="col-md-4"></div>
  	<div class="col-md-4">
              <p> {{data['host'] }} </p>
             <img style="-webkit-user-select: none" src="http://192.168.1.18:8081/">
<a href="/snapshot" ><button class="btn btn-success">Take Snapshot</button></a>
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
                 % for x in data['data']:
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


