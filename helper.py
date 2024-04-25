screen_helper = """

ScreenManager:
    LoginScreen:
    RegisterScreen:
    WelcomeScreen:
    HomeScreen:
    SleepTrackingScreen:
    FeedingTrackingScreen:
    GrowthHealthTrackingScreen:
    LullabiesScreen:
    VideoScreen:
    SleepEntryScreen:
    FeedingEntryScreen:
    AccountScreen:
    UpdateBabyScreen:

<LoginScreen>:
    name: 'Login'
    MDLabel:
        text: "Please log in to continue"
        theme_text_color: "Primary"
        halign: "center"
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        
    MDTextField:
        id: login_username
        hint_text: "Enter username"
        icon_right: "account-box"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.7}
        size_hint_x: None
        width: 300
        
    MDTextField:
        id: login_password
        hint_text: "Enter password"
        password: True
        helper_text: "Forgot password?"
        helper_text_mode: "on_focus"
        icon_right: "lock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.6}
        size_hint_x: None
        width: 300
        
    MDFillRoundFlatButton:
        text: "Log in"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: app.login(root.ids.login_username.text, root.ids.login_password.text)
        
    MDFillRoundFlatButton:
        text: "Create an account"
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        on_press: root.manager.current = 'Register'
        
        
        
<RegisterScreen>:
    name: 'Register'
    MDLabel:
        text: "Create a new account"
        theme_text_color: "Primary"
        halign: "center"
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        
    MDTextField:
        id: username
        hint_text: "Create an username"
        helper_text_mode: "on_error"
        icon_right: "account-box"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.7}
        size_hint_x: None
        width:300
        
    MDTextField:
        id: password
        hint_text: "Create a password"
        icon_right: "lock"
        password: True
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.6}
        size_hint_x: None
        width:300
        
    MDTextField:
        id: first_name
        hint_text: "First Name"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        size_hint_x: None
        width:300
        
    MDTextField:
        id: last_name
        hint_text: "Last Name"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.4}
        size_hint_x: None
        width:300
        
    MDFillRoundFlatButton:
        text: "Create an account"
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_release: app.create_account(root.ids.username.text, root.ids.password.text, root.ids.first_name.text, root.ids.last_name.text)
        
    MDFillRoundFlatButton:
        text: "Back"
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        on_release: app.back_to_login()
          
        
<WelcomeScreen>:
    name: 'Welcome'
    MDLabel:
        text: "Welcome to BabyV!"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1
        font_style: "H5"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
          
    MDTextField:
        id: baby_name
        hint_text: "Baby Name"
        helper_text_mode: "on_error"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.75}
        size_hint_x: None
        width:300
        mode: "rectangle"
        
    MDTextField:
        id: date_of_birth
        hint_text: "Date of birth"
        icon_right: "calendar-today"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.65}
        size_hint_x: None
        width: 300
        mode: "rectangle"
        on_focus: if self.focus: app.show_date_picker(1)
        readonly: True
        
    MDTextField:
        id: hour_of_birth
        hint_text: "Hour of birth"
        icon_right: "clock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.55}
        size_hint_x: None
        width: 300
        mode: "rectangle"
        on_focus: if self.focus: app.show_time_picker()
        readonly: True
        
    MDTextField:
        id: birth_weight
        hint_text: "Weight at birth (kg)"
        icon_right: "baby-carriage"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.45}
        size_hint_x: None
        width: 300
        input_type: 'number'
        mode: "rectangle"
        
    MDTextField:
        id: birth_height
        hint_text: "Height at birth (cm)"
        icon_right: "human-male-height"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.35}
        size_hint_x: None
        width: 300
        input_type: 'number'
        mode: "rectangle"
        
    MDFloatingActionButton:
        icon: 'check-bold'
        elevation_normal: 12
        md_bg_color: 0.9, 0.68, 0.86, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_release: root.save_baby_details(root.ids.baby_name.text, root.ids.date_of_birth.text, root.ids.hour_of_birth.text, root.ids.birth_weight.text, root.ids.birth_height.text)
        
    MDFillRoundFlatButton:
        text: "Skip for now"
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        on_press: root.manager.current = 'Home'
  
<AccountScreen>:
    name: 'Account'
    MDLabel:
        text: "Manage your Account"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 0.9, 0.68, 0.86, 1
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        
    MDIconButton:
        icon: root.icon_lights
        elevation_normal: 12
        pos_hint: {'center_x': 0.9, 'center_y': 0.9}
        on_press: root.toggle_icon_lights()

    MDTextField:
        id: password
        hint_text: "Update password"
        helper_text_mode: "on_error"
        pos_hint: {'center_x': 0.35, 'center_y': 0.7}
        size_hint_x: None
        width: 250
        
    MDFloatingActionButton:
        icon: 'check-bold'
        elevation_normal: 12
        md_bg_color: 0.9, 0.68, 0.86, 1
        pos_hint: {'center_x': 0.75, 'center_y': 0.7}
        on_press: root.update_password()

    MDTextField:
        id: first_name
        hint_text: "Update first name"
        helper_text_mode: "on_error"
        pos_hint: {'center_x': 0.35, 'center_y': 0.6}
        size_hint_x: None
        width: 250
        
    MDFloatingActionButton:
        icon: 'check-bold'
        elevation_normal: 12
        md_bg_color: 0.9, 0.68, 0.86, 1
        pos_hint: {'center_x': 0.75, 'center_y': 0.6}
        on_press: root.update_first_name()

    MDTextField:
        id: last_name
        hint_text: "Update last name"
        helper_text_mode: "on_error"
        pos_hint: {'center_x': 0.35, 'center_y': 0.5}
        size_hint_x: None
        width: 250
        
    MDFloatingActionButton:
        icon: 'check-bold'
        elevation_normal: 12
        md_bg_color: 0.9, 0.68, 0.86, 1
        pos_hint: {'center_x': 0.75, 'center_y': 0.5}
        on_press: root.update_last_name()
        
    MDFillRoundFlatButton:
        text: "Update baby info"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_press: root.manager.current = 'UpdateBaby'
        
    MDFillRoundFlatButton:
        text: "Logout"
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        on_press: root.manager.current = 'Login'
        
    MDRaisedButton:
        text: "Delete your account"
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        md_bg_color: 0.9, 0.68, 0.86, 1
        on_press: root.show_delete_confirmation()
        
    MDFillRoundFlatButton:
        text: "Back"
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_press: root.manager.current = 'Home'

<UpdateBabyScreen>:
    name: 'UpdateBaby'
        
        
<HomeScreen>:        
    name: 'Home'
    MDLabel:
        text: "Home"
        theme_text_color: "Custom"
        text_color: 0.9, 0.68, 0.86, 1
        halign: "center"
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.85}
        
    MDIconButton:
        icon: "account-details"
        size_hint: None, None
        size: dp(150), dp(150) 
        pos_hint: {'center_x': 0.1, 'center_y': 0.95}
        on_press: root.manager.current = 'Account'
        elevation_normal: 12

    MDLabel:
        text: f"{root.first_name} {root.last_name}"
        pos_hint: {'center_x': 0.35, 'center_y': 0.95}
        halign: "center"
        width:300
        
    MDFillRoundFlatButton:
        text: "Sleep Tracking"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        on_press: root.manager.current = 'SleepTracking'
        
    MDFillRoundFlatButton:
        text: "Feeding Tracking"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        on_press: root.manager.current = 'FeedingTracking'
        
    MDFillRoundFlatButton:
        text: "Growth & Health Tracking"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_press: root.manager.current = 'GrowthHealthTracking'
        
    MDFillRoundFlatButton:
        text: "Lullabies & White Noise"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_press: root.manager.current = 'Lullabies'
        
    MDFloatingActionButton:
        icon: 'video-outline'
        pos_hint: {'center_x': 0.4, 'center_y': 0.2}
        md_bg_color: 0.9, 0.68, 0.86, 1
        on_press: root.manager.current = 'Video'
        size: dp(150), dp(150)
        elevation_normal: 12
        
        
    MDFloatingActionButton:
        icon: root.icon_audio
        size_hint: None, None
        md_bg_color: 0.9, 0.68, 0.86, 1
        size: dp(150), dp(150) 
        pos_hint: {'center_x': 0.6, 'center_y': 0.2}
        on_press: root.toggle_icon_audio()
        elevation_normal: 12
       
        
<SleepTrackingScreen>:        
    name: 'SleepTracking'
    BoxLayout:
        id: sleep_graph
    
    MDLabel:
        text: "Sleep Tracking"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 0.9, 0.68, 0.86, 1
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        
    MDLabel:
        text: "Baby ... has slept today ... hours!"
        halign: "center"
        theme_text_color: "Secondary"
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        
    MDFloatingActionButton:
        icon: "plus"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        md_bg_color: 0.9, 0.68, 0.86, 1
        on_press: root.manager.current = 'SleepEntry'
        
    MDFillRoundFlatButton:
        text: "Sleep History"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        on_release: root.plot_sleep_chart_call()
        #on_release: root.create_sleep_chart()
        
    MDFillRoundFlatButton:
        text: "Back"
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        on_press: root.manager.current = 'Home'
        
    
    
    
<SleepEntryScreen>:        
    name: 'SleepEntry'
    
    MDLabel:
        text: "Add new sleep entry"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 0.9, 0.68, 0.86, 1
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        
    MDTextField:
        id: start_hour
        hint_text: "Start Hour"
        helper_text_mode: "on_error"
        icon_right: "clock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.7}
        size_hint_x: None
        width: 300
        mode: "rectangle"
        on_focus: if self.focus: app.show_time_picker_for_sleep_entry(1)
        readonly: True
        
    MDTextField:
        id: end_hour
        hint_text: "End Hour"
        helper_text_mode: "on_error"
        icon_right: "clock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.6}
        size_hint_x: None
        width: 300
        mode: "rectangle"
        on_focus: if self.focus: app.show_time_picker_for_sleep_entry(0)
        readonly: True
        
    MDTextField:
        id: sleep_date
        hint_text: "Date"
        helper_text_mode: "on_error"
        icon_right: "calendar-today"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        size_hint_x: None
        width: 300
        mode: "rectangle"
        on_focus: if self.focus: app.show_date_picker(2)
        readonly: True
        
    MDTextField:
        id: sleep_notes
        hint_text: "Notes"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.4}
        size_hint_x: None
        width:300
        mode: "rectangle"
        
    MDFloatingActionButton:
        icon: "check-bold"
        md_bg_color: 0.9, 0.68, 0.86, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        on_release: root.add_sleep_entry("", root.ids.start_hour.text, root.ids.end_hour.text, root.ids.sleep_date.text, root.ids.sleep_notes.text)
        
    MDFillRoundFlatButton:
        text: "Back"
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_press: root.manager.current = 'SleepTracking'
    
    
    
<FeedingTrackingScreen>:        
    name: 'FeedingTracking'
    
    MDLabel:
        text: "Feeding Tracking"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 0.9, 0.68, 0.86, 1
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        
    MDLabel:
        text: "Baby ... has ate today ... times!"
        halign: "center"
        theme_text_color: "Secondary"
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        
    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: 0.9, 0.68, 0.86, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        on_press: root.manager.current = 'FeedingEntry'
        
    MDFillRoundFlatButton:
        text: "Feeding History"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        #on_release: root.plot_sleep_chart_call()
        
    MDFillRoundFlatButton:
        text: "Back"
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        on_press: root.manager.current = 'Home'
    
    

<FeedingEntryScreen>:        
    name: 'FeedingEntry'
    
    MDLabel:
        text: "Add new feeding entry"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 0.9, 0.68, 0.86, 1
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        
    MDTextField:
        id: feed_hour
        hint_text: "Feed Hour"
        icon_right: "clock"
        helper_text_mode: "on_error"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.8}
        size_hint_x: None
        width: 300
        mode: "rectangle"
        on_focus: if self.focus: app.show_time_picker_for_feed()
        readonly: True
        
    MDTextField:
        id: feed_date
        hint_text: "Date"
        helper_text_mode: "on_error"
        icon_right: "calendar-today"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.7}
        size_hint_x: None
        width: 300
        mode: "rectangle"
        on_focus: if self.focus: app.show_date_picker(3)
        readonly: True
        
    MDTextField:
        id: feed_notes
        hint_text: "What did your baby eat?"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.5, 'center_y':0.6}
        size_hint_x: None
        width:300
        mode: "rectangle"
        
    MDLabel:
        text: "Milk amount: {} ml".format(int(milk_slider.value))
        halign: 'center'
        size_hint_y: None
        height: '48dp'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        
    MDSlider:
        id: milk_slider
        min: 0
        max: 300
        value: 150
        orientation: 'horizontal'
        show_off: False
        size_hint_y: None
        height: '200dp'
        pos_hint: {'center_x':0.5, 'center_y':0.4}
    
    MDFloatingActionButton:
        icon: "check-bold"
        md_bg_color: 0.9, 0.68, 0.86, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_release:  root.add_food_entry("", root.ids.feed_hour.text, root.ids.feed_date.text, int(root.ids.milk_slider.value), root.ids.feed_notes.text)
        
    MDFillRoundFlatButton:
        text: "Back"
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        on_press: root.manager.current = 'FeedingTracking'

    
    
<GrowthHealthTrackingScreen>:        
    name: 'GrowthHealthTracking'
    
    MDLabel:
        text: "Growth & Health Tracking"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 0.9, 0.68, 0.86, 1
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        
        
    MDFillRoundFlatButton:
        text: "Back"
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        on_press: root.manager.current = 'Home'



<LullabiesScreen>:        
    name: 'Lullabies'    
    
    MDLabel:
        text: "Lullabies"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 0.9, 0.68, 0.86, 1
        font_style: "H6"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}    
    
    ScrollView:
        do_scroll_x: False
        size_hint: 0.8, 0.6
        pos_hint: {'center_x': 0.6, 'center_y': 0.5}
        GridLayout:
            id: content
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(10)
            padding: dp(10)

    MDFillRoundFlatButton:
        text: "Back"
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        on_press: root.manager.current = 'Home'
        
 
    
<VideoScreen>:        
    name: 'Video'
            
    VideoStreamWidget:
        id: video_stream
        size_hint: None, None
        size: root.width, root.height
        pos: 0, 0
        
    MDFloatingActionButton:
        icon: root.icon
        size_hint: None, None
        size: dp(150), dp(150) 
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_press: root.toggle_icon()
        elevation_normal: 12
        
    MDFillRoundFlatButton:
        text: "Back"
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        on_press: root.manager.current = 'Home'
"""