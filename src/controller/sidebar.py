from gi.repository import Gtk
import threading

from model.trace_utils import TraceUtils, Str


@Gtk.Template(filename="ui/sidebar.ui")
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

    def __init__(self, *args, **kwargs):
        super().__init__(* args, **kwargs)

        # object members for kernel methods
        self.single_select_kernel = Gtk.SingleSelection()
        self.filter_model_kernel = Gtk.FilterListModel()
        self.single_select_user = Gtk.SingleSelection()
        self.filter_model_user = Gtk.FilterListModel()
        self.search_filter = Gtk.CustomFilter()

        # scrolling
        self.kernel_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.user_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        TraceUtils.get_kernel_methods()
        self.set_kernel_list_view()

    @Gtk.Template.Callback()
    def on_search_changed(self, *args):
        active_child = self.get_active_stack()
        if active_child == "Kernel":
            self.search_filter.set_filter_func(self.filter_func, self.filter_model_kernel)
        elif active_child == "File":
            self.search_filter.set_filter_func(self.filter_func, self.filter_model_user)
        else:
            pass

    def get_active_stack(self):
        return self.sidebar_stack.get_visible_child_name()

    def set_kernel_list_view(self):
        self.filter_model_kernel.set_model(TraceUtils.kernel_methods)
        self.search_filter.set_filter_func(self.filter_func, self.filter_model_kernel)
        self.filter_model_kernel.set_filter(self.search_filter)
        self.single_select_kernel.set_model(self.filter_model_kernel)

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", lambda _fact, item:
            item.set_child(Gtk.Label(halign=Gtk.Align.START)))
        factory.connect("bind", lambda _fact, item:
            item.get_child().set_label(item.get_item().value))

        self.methods_from_kernel.set_model(self.single_select_kernel)
        self.methods_from_kernel.set_factory(factory)

    def set_user_list_view(self):
        self.filter_model_user.set_model(TraceUtils.user_methods)
        self.search_filter.set_filter_func(self.filter_func, self.filter_model_user)
        self.filter_model_user.set_filter(self.search_filter)
        self.single_select_user.set_model(self.filter_model_user)

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", lambda _fact, item:
            item.set_child(Gtk.Label(halign=Gtk.Align.START)))
        factory.connect("bind", lambda _fact, item:
            item.get_child().set_label(item.get_item().value))

        self.methods_from_user.set_model(self.single_select_user)
        self.methods_from_user.set_factory(factory)

    def filter_func(self, method, *args):
        query = self.search_entry.get_text()
        if not query:
            return True
        query = query.casefold()

        if query in method.value.casefold():
            return True

        return False

    def set_user_methods(self, file_path):
        TraceUtils.get_user_methods(file_path)
        self.set_user_list_view()

    def get_selected_method(self):
        active_child = self.get_active_stack()
        if active_child == "Kernel" and self.single_select_kernel.get_selected_item() is not None:
            return self.single_select_kernel.get_selected_item().get_value()
        elif active_child == "File" and self.single_select_user.get_selected_item() is not None:
            return self.single_select_user.get_selected_item().get_value()
        else:
            return None

    def get_selected_file(self):
        if self.get_active_stack() == "File":
            return TraceUtils.file
        else:
            return None
