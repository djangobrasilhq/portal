from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Administração customizada para o modelo User"""

    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser",
        "created_at",
        "social_links",
    ]

    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name",
    ]

    list_filter = [
        "is_staff",
        "is_active",
        "is_superuser",
        "created_at",
    ]

    list_editable = ["is_active"]

    ordering = ["-created_at"]

    list_per_page = 25

    fieldsets = (
        (
            "Informações Básicas",
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                )
            },
        ),
        (
            "Informações Pessoais",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "bio",
                )
            },
        ),
        (
            "Links Sociais",
            {
                "fields": (
                    "gitlab",
                    "gitbucket",
                    "linkedin",
                    "twitter",
                    "website",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Datas Importantes",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


    readonly_fields = [
        "last_login",
        "date_joined",
        "created_at",
        "updated_at",
    ]

    @admin.display(description="Links Sociais")
    def social_links(self, obj):
        """Exibe links sociais de forma visual"""
        links = []
        if obj.gitlab:
            links.append(
                format_html(
                    '<a href="{}" target="_blank" style="color: #FC6D26;">GitLab</a>',
                    obj.gitlab,
                )
            )
        if obj.gitbucket:
            links.append(
                format_html(
                    '<a href="{}" target="_blank" style="color: #0052CC;">Bitbucket</a>',
                    obj.gitbucket,
                )
            )
        if obj.linkedin:
            links.append(
                format_html(
                    '<a href="{}" target="_blank" style="color: #0077B5;">LinkedIn</a>',
                    obj.linkedin,
                )
            )
        if obj.twitter:
            links.append(
                format_html(
                    '<a href="https://twitter.com/{}" target="_blank" style="color: #1DA1F2;">Twitter</a>',
                    obj.twitter.replace("@", ""),
                )
            )
        if obj.website:
            links.append(
                format_html(
                    '<a href="{}" target="_blank" style="color: #44B78B;">Website</a>',
                    obj.website,
                )
            )

        if links:
            return mark_safe(" | ".join(str(link) for link in links))
        return mark_safe('<span style="color: #999;">Nenhum link</span>')
