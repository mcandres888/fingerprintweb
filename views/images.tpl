% include('header.tpl')
    <div class="container theme-showcase" role="main">
      <div class="row">

 <div class="col-lg-12">
                <h1 class="page-header">Captured Images</h1>
            </div>

        % for x in data['data']:
            <div class="col-lg-3 col-md-4 col-xs-6 thumb">
                <a class="thumbnail" href="/image/{{x['id']}}/{{x['path']}}">
                    <img class="img-responsive" src="/public/images/{{x['path']}}" alt="">
                    <!-- <img class="img-responsive" src="http://placehold.it/400x300" alt=""> -->
                </a>
            </div>
        % end


      </div>
    </div> <!-- /container -->

% include('footer.tpl')


