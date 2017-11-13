""" Work with the database """
import uuid
import xmltodict


from black.db import Sessions, ScanDatabase


def save_raw_output(task_id, output, project_uuid):
    try:
        sessions = Sessions()
        concated = "".join(output)

        if concated:
            parsed_dict = xmltodict.parse(concated)

            session = sessions.get_new_session()

            if isinstance(parsed_dict['nmaprun']['host'], list):
                for each_host in parsed_dict['nmaprun']['host']:
                    address = each_host['address']['@addr']
                    port_data = each_host['ports']['port']

                    protocol = port_data['@protocol']
                    port_number = int(port_data['@portid'])

                    port_state = port_data['state']
                    port_status = port_state['@state']

                    if port_state != 'closed':
                        new_scan = ScanDatabase(
                            scan_id=str(uuid.uuid4()),
                            target=address,
                            port_number=port_number,
                            task_id=task_id,
                            project_uuid=project_uuid)

                        session.add(new_scan)
                        session.commit()
            else:
                each_host = parsed_dict['nmaprun']['host']
                address = each_host['address']['@addr']
                port_data = each_host['ports']['port']

                protocol = port_data['@protocol']
                port_number = int(port_data['@portid'])

                port_state = port_data['state']
                port_status = port_state['@state']

                if port_state != 'closed':
                    new_scan = ScanDatabase(
                        scan_id=str(uuid.uuid4()),
                        target=address,
                        port_number=port_number,
                        task_id=task_id,
                        project_uuid=project_uuid)

                    session.add(new_scan)
                    session.commit()

            sessions.destroy_session(session)

    except Exception as e:
        # TODO: add logger here
        print("save_raw_output")
        print(e)
        raise e
