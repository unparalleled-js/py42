import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class ArchiveClient(BaseClient):
    def get_data_key_token(self, device_guid):
        uri = u"/api/DataKeyToken"
        data = {u"computerGuid": device_guid}
        return self._session.post(uri, data=json.dumps(data))

    def get_backup_sets(self, device_guid, destination_guid):
        uri = u"/c42api/v3/BackupSets/{}/{}".format(device_guid, destination_guid)
        return self._session.get(uri)

    def get_all_restore_history(self, days, id_type, id_value, **kwargs):
        return get_all_pages(
            self._get_restore_history_page,
            u"restoreEvents",
            days=days,
            id_type=id_type,
            id_value=id_value,
            **kwargs
        )

    def _get_restore_history_page(self, days, id_type, id_value, page_num, page_size, **kwargs):
        uri = u"/api/RestoreHistory"
        params = dict(days=days, pgNum=page_num, pgSize=page_size, **kwargs)
        params[id_type] = id_value
        return self._session.get(uri, params=params)

    def get_web_restore_info(self, src_guid, dest_guid):
        uri = u"/api/WebRestoreInfo"
        params = {u"srcGuid": src_guid, u"destGuid": dest_guid}
        return self._session.get(uri, params=params)

    def get_all_cold_storage_archives_by_org_id(
        self, org_id, inc_child_orgs=True, sort_key=None, sort_dir="asc"
    ):
        pass

    def get_all_cold_storage_archives_by_destination_guid(
        self, destination_guid, sort_key=None, sort_dir="asc"
    ):
        pass

    def update_cold_storage_purge_date(self, archive_guid, purge_date):
        uri = u"/api/coldStorage/{0}".format(archive_guid)
        params = {u"idType": u"guid"}
        data = {u"archiveHoldExpireDate": purge_date}
        return self._session.put(uri, params=params, data=json.dumps(data))
