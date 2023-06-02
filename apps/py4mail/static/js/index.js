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
    mailOption: 0, // 0 = list, 1 = individual mail
    mail: {}
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

    //One function with a 
    //param of `type` to get the mails from inbox, trash, or starred
    getGlobal: function(type) {
      app.vue.mailOption = 0;
      axios.get(get_emails_url).then(function(response) {
        app.data.emails_as_dict = {};
        app.vue.emails = app.enumerate(response.data.emails).filter(function(email) {
          if (type) {
            app.data.emails_as_dict[email.id] = email;
            return true;
          }
          return false;
        });
        app.methods.formatEmailsByTime();
      });
    },

    //get the mails from inbox
    getInbox: function() {
      app.methods.getGlobal(email.isTrash === null);
    },    

    //get the mails from trash
    getTrash: function() {
      app.methods.getGlobal(email.isTrash === true);
    },

    //get the mails from starred
    getStarred: function() { 
      app.methods.getGlobal(email.isStarred === true);
    },

    // view individual mail 
    viewMail: function(email_id) {
      console.log(email_id);
      app.vue.mailOption = 1; //switch to individual mail
      app.vue.mail = email_id;
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
    //get mails from inbox by default
    app.methods.getInbox();
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it.
init(app);

