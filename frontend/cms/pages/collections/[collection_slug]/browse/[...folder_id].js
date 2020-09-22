import React from "react";
import { useRouter } from "next/router";
import { useAPI } from "hooks";
import { Link, Loading } from "components";
import { Folder, Media, FileBrowser } from "components/filebrowser";
import Breadcrumbs from "components/navigation/breadcrumbs";

const CollectionBrowser = (props) => {
  const router = useRouter();

  const { collection_slug, folder_id } = router.query;

  // conditionally fetch content if collection_slug and folder_id present
  const { data } = useAPI(collection_slug && folder_id ? `/api/sets/` : null, {
    collection: collection_slug,
    set: folder_id,
  });

  if (!data) {
    return <Loading />;
  }

  const { name = "", children = [], ancestors = [], mediaEntries = [] } = data;

  return (
    <>
      <h1>{name}</h1>
      <Breadcrumbs>
        {ancestors.map((a) => (
          <Link
            key={`set-${a.id}`}
            href={`/collections/${collection_slug}/browse/${a.id}/`}
          >
            <a>{a.name}</a>
          </Link>
        ))}
      </Breadcrumbs>

      <FileBrowser>
        {children.map((c) => (
          <Link
            key={`set-${c.id}`}
            href={router.pathname}
            as={`/collections/${collection_slug}/browse/${c.id}/`}
          >
            <a>
              <Folder name={c.name} />
            </a>
          </Link>
        ))}
        {mediaEntries.map((media) => (
          <Link
            key={`media-${media.id}`}
            href={`/collections/[collection_slug]/media/[media_id]/`}
            as={`/collections/${collection_slug}/media/${media.id}/`}
          >
            <a>
              <Media {...media} />
            </a>
          </Link>
        ))}
      </FileBrowser>
      {/* <pre>{JSON.stringify({ props, data }, null, 2)}</pre> */}
    </>
  );
};

export default CollectionBrowser;
