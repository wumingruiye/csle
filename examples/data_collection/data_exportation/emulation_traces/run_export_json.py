from csle_common.util.export_util import ExportUtil

if __name__ == '__main__':
    ExportUtil.export_emulation_traces_to_disk_json(
        num_traces_per_file=100, output_dir="/home/kim/traces_2_aug_22_json",
        zip_file_output="/home/kim/traces_2_aug_22_json.zip", max_num_traces=2000, added_by="Kim Hammar")