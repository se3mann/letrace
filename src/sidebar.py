from gi.repository import Gtk
from trace_utils import TraceUtils, Str


@Gtk.Template(filename="sidebar.ui")
class TraceSideBar(Gtk.Box):
    __gtype_name__ = 'TraceSideBar'

    search_entry = Gtk.Template.Child()
    sidebar_switcher = Gtk.Template.Child()
    sidebar_stack = Gtk.Template.Child()
    kernel_stackpage = Gtk.Template.Child()
    user_stackpage = Gtk.Template.Child()
    user_scrolled_window = Gtk.Template.Child()
    kernel_scrolled_window = Gtk.Template.Child()
    methods_from_user = Gtk.Template.Child()
    methods_from_kernel = Gtk.Template.Child()
    
    #models for ListView
    single_select_kernel = Gtk.SingleSelection()
    single_select_user = Gtk.SingleSelection()
    filter_model = Gtk.FilterListModel()
    str_filter = Gtk.StringFilter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # connect the search bar to the search callback
        # self.search_entry.connect("search-changed", self.on_search_changed)
        # scrolling settings
        self.kernel_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.user_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.set_sidebar()
        print("Sidebar init")
        TraceUtils.test_list.append(Str("test1 ez egy nagyon hosszú szöveg ám, tényleg"))
        TraceUtils.test_list.append(Str("test2"))
        TraceUtils.test_list.append(Str("test3"))
        for i in range(50):
            TraceUtils.test_list.append(Str(f"test{i}"))
            


    def get_active_stack(self):
        return self.sidebar_stack.get_visible_child_name()
    
    def set_sidebar(self):
        # for searching
        self.filter_model.set_model(TraceUtils.test_list)
        # Filter
        self.str_filter.set_search(self.search_entry.get_text())
        self.str_filter.set_ignore_case(True)
        self.str_filter.set_match_mode(Gtk.StringFilterMatchMode.SUBSTRING)
        self.filter_model.set_filter(self.str_filter)
        
        self.single_select_kernel.set_model(self.filter_model)
        
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", lambda _fact, item:
            item.set_child(Gtk.Label(halign=Gtk.Align.START)))
        factory.connect("bind", lambda _fact, item:
            item.get_child().set_label(item.get_item()._value))
        
        self.methods_from_kernel.set_model(self.single_select_kernel)
        self.methods_from_kernel.set_factory(factory)

    @Gtk.Template.Callback()
    def on_search_activate(self, *args):
        print("search activate")

    @Gtk.Template.Callback()
    def on_search_changed(self, *args):
        active_child = self.get_active_stack()
        if active_child == "Kernel":
            print("kernel stackpage")
            self.str_filter.set_search(self.search_entry.get_text())
            
            
        elif active_child == "File":
            print("user stackpage")
        else:
            print("else")
            pass


    def setup_single_select_listview(self, data):
        # for searching
        filter_model = Gtk.FilterListModel(model=TraceUtils.test_list)
        # Filter
        str_filter = Gtk.StringFilter()
        str_filter.set_search(self.search_entry.get_text())
        str_filter.set_ignore_case(True)
        str_filter.set_match_mode(Gtk.StringFilterMatchMode.SUBSTRING)
        filter_model.set_filter(str_filter)
        
        self.single_select_kernel.set_model(filter_model)
        # factory for ListView widget, it is needed to display the list
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", lambda _fact, item:
            item.set_child(Gtk.Label(halign=Gtk.Align.START)))
        factory.connect("bind", lambda _fact, item:
            item.get_child().set_label(item.get_item()._value))

        self.methods_from_kernel.set_model(self.single_select_kernel)
        self.methods_from_kernel.set_factory(factory)
