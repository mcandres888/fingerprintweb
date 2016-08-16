% include('header.tpl')
    <div class="container theme-showcase" role="main">
      <div class="row">
        <div class="col-xs-12">
          <table class="table table-bordered table-condensed table-responsive ">
            <thead>
              <tr>
                <th>Id</th>
                <th>Name</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
            % for x in data['data']:
              <tr>
                <form action="/fingerprintupdate" method="post">
                <input type="hidden" name="finger_id" value="{{x['id']}}">
                <td>{{x['id']}}</td>
                <td><input  type="text" name="finger_name" value="{{x['name']}}"/></td>
               <td><button type="submit" class="btn btn-success">Update</button></td>
               </form>
              </tr>
             % end
            </tbody>
          </table>
        </div>
      </div>


    </div> <!-- /container -->

% include('footer.tpl')


