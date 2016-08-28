% include('header.tpl')
    <div class="container theme-showcase" role="main">
      <div class="row">
           <div class="span7 center"> 
             <img style="-webkit-user-select: none" src="http://{{data['host']}}:8081/">
      </div>
      </div>
      <div class="row">
           <div class="span7 center"> 
<a href="/snapshot" ><button class="btn btn-success">Take Snapshot</button></a>
      </div>
      </div>
      <div class="row">
          <table class="table table-hover">
              <thead>
                 <tr>
			<th> Time </th>
                 	<th> Type </th>
                 	<th> Notes </th>
                 	<th> Image </th>
                 	<th> Action </th>
		</tr>
              </thead>
              <tbody>
                 % for x in data['data']:
                 <tr>
			<td> {{x['time']}} </td>
                 	<td> {{x['type']}} </td>
                 	<td> {{x['note']}} </td>
                 	<td> <a href="http://{{data['host']}}/image/{{x['image']}}"> Picture </a> </td>
                 	<td> <a href="http://{{data['host']}}/activity/delete/{{x['id']}}"> Delete </a> </td>
		</tr>
                % end
              </tbody>
       
          </table>
      </div>


    </div> <!-- /container -->

% include('footer.tpl')


