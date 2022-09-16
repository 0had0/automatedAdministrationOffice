from auth.manager import MyAccountManager


class DirectorManager(MyAccountManager):

    def create_user(self, **kwargs):
        return MyAccountManager.create_user(self, **kwargs, is_director=True)


class UserManager(MyAccountManager):

    def create_user(self, **kwargs):
        return MyAccountManager.create_user(self, **kwargs, is_director=False)


class ReviewerManager(MyAccountManager):

    def create_user(self, **kwargs):
        return MyAccountManager.create_user(self, **kwargs, is_director=False, is_reviewer=True)
