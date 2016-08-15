% include('header.tpl')
    <div class="container theme-showcase" role="main">
      <div class="row">
        <div class="col-xs-12">
 	   <h2> Updating Finger print for {{data['name']}}</h2>
          <div class="row">
          <div class="col-md-6">
            <ol>
              <li><h3> Wait for the finger print scanner to open</h3></li>
              <li><h3> Place your finger on the scanner</h3></li>
              <li><h3> It will beep when its done</h3></li>
              <li><h3> Place your finger again on the scanner</h3></li>
              <li><h3> Then your good to go!</h3></li>
            </ol>
          </div>
          <div class="col-md-6">
          <img class="img-responsive" src="/public/images/fingerprint.png" alt="fingerprint" class="img-rounded">
          </div>
          </div>
          <div class="row">
           <a href="/"><button type="button" class="btn btn-success">Go back and enable Security</button></a>
          </div>
        </div>
      </div>


    </div> <!-- /container -->

% include('footer.tpl')


