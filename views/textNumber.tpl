% include('header.tpl')
    <div class="container theme-showcase" role="main">
      <div class="row">
        <div class="col-xs-12">
          <table class="table table-bordered table-condensed table-responsive ">
            <thead>
              <tr>
                <th>Mobile Number</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
            % for x in data['data']:
              <tr>
                <form action="/textnumberupdate" method="post">
                <input type="hidden" name="mobile_id" value="{{x['id']}}">
                <td><input  type="text" name="mobile_number" value="{{x['mobile_number']}}"/></td>
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


