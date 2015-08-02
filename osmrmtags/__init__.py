from imposm.parser import OSMParser
from osmwriter import OSMWriter

def rm_tags(tags, tags_to_keep):
    new_tags = {}
    for ok_tag in tags_to_keep:
        if ok_tag in tags:
            new_tags[ok_tag] = tags[ok_tag]

    return new_tags

class TagRemover(object):
    def __init__(self, output_writer, tags_to_keep):
        self.output_writer = output_writer
        self.tags_to_keep = tags_to_keep

    
    def nodes(self, nodes):
        for node in nodes:
            id, tags, (lat, lon) = node
            new_tags = rm_tags(tags, self.tags_to_keep)
            self.output_writer.node(id, lat, lon, new_tags)

    def ways(self, ways):
        for way in ways:
            id, tags, nodes = way
            new_tags = rm_tags(tags, self.tags_to_keep)

            if len(tags) > 0:
                self.output_writer.way(id, new_tags, nodes)


def remove_tags(input_filename, output_fp, tags_to_keep, close_output_fp=True):

    output_writer = OSMWriter(fp=output_fp)
    remover = TagRemover(output_writer, tags_to_keep)
    parser = OSMParser(ways_callback=remover.ways, nodes_callback=remover.nodes, concurrency=1)
    parser.parse(input_filename)

    output_writer.close(close_file=close_output_fp)


def main(argv=None):
    argv = argv or sys.argv[1:]


    input_filename, output_filename, tags_to_keep = argv
    tags_to_keep = tags_to_keep.split(",")

    with open(output_filename, "w") as output_fp:
        remove_tags(input_filename, output_fp, tags_to_keep, close_output_fp=True)


if __name__ == '__main__':
    main(sys.argv[1:])
