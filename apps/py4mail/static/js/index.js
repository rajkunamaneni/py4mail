// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
  // This is the Vue data.
  app.data = {
    emails: [],
    emails_as_dict: {},
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  // This contains all the methods.
  app.methods = {
    formatEmailsByTime: function () {
      app.vue.emails.sort(function (a, b) {
        return new Date(b.sent_at) - new Date(a.sent_at);
      });
    },
    // Complete as you see fit.
    getTrash: function() {
      axios.get(get_trash).then(function (response) {
        app.vue.emails = app.enumerate(response.data.emails);
      })
    },
    
    getStarred: function() {  
      axios.get(get_emails_url).then(function (response) {
        app.vue.emails = app.enumerate(response.data.emails);
      });
    },
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // And this initializes it.
  app.init = () => {
    axios.get(get_emails_url).then(function (response) {
      app.vue.emails = app.enumerate(response.data.emails);
      app.vue.emails.map(function(email) {
        console.log(email);
        app.data.emails_as_dict[email.id] = email;
      });
      app.methods.formatEmailsByTime();
    });
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it.
init(app);

